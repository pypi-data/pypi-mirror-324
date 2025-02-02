import os
import pickle
from multiprocessing.spawn import prepare

from django.conf import settings
from cryptography.fernet import Fernet
from django.db import connection
from django.core.management import call_command
from django.db.utils import ConnectionDoesNotExist
from django.db import connections, DEFAULT_DB_ALIAS
from contextlib import contextmanager
from types import SimpleNamespace

class Script_db_Manager:
    def __init__(self, script, project):
        self.script = script
        self.project = project
        print(f"settings.DATABASES: {settings.DATABASES}")
        self.db_alias = self.get_db_alias()
        self.encryption_key = self.get_encryption_key()
        print("Using database for project:", self.db_alias)

    def get_encryption_key(self):
        with self.using_project_db() as connection:
            with connection.cursor() as cursor:
                # Ensure project_id is passed as an integer
                project_id = int(self.project.id)  # Convert to integer explicitly
                print(project_id)
                query = "SELECT encryption_key FROM encryption_keys WHERE project_id = {}".format(project_id)
                cursor.execute(query)
                result = cursor.fetchone()
                key = result[0]
                # Return the encryption key if found, otherwise None
                return key

    def get_db_alias(self):
        print(f"Looking for project ID: {self.project.id}")
        print(f"Available connections: {connections.databases.keys()}")
        project_id = str(self.project.id)  # Assuming project has an `id` attribute
        if project_id in connections.databases:
            print(connections.databases)
            return project_id
        else:
            raise ValueError(f"No database configuration found for project ID: {project_id}")

    @contextmanager
    def using_project_db(self):

        db_alias = self.db_alias  # The database alias for the project
        try:
            # Ensure the database alias exists
            if db_alias not in connections.databases:
                raise ValueError(f"Database alias '{db_alias}' does not exist.")

            yield connections[db_alias]
        finally:

            pass


    def get_project_scripts(self):
        table_name = f"project_scripts"
        with self.using_project_db() as connection:
            with connection.cursor() as cursor:
                query = f"""
                    SELECT *
                    FROM {table_name};
                """
                cursor.execute(query,)
                results = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                print(column_names)
                # Fetch all rows
                print(results)
                scripts = [
                    {
                        'id': row[0],
                        'test_name': row[1],
                        'script_version': row[2],
                    }
                    for row in results
                ]
                return scripts


    def encrypt_data(self, data):
        fernet = Fernet(self.encryption_key)
        return fernet.encrypt(pickle.dumps(data))

    def decrypt_pickle_data(self, encrypted_data):

        return pickle.loads(fernet.decrypt(encrypted_data))

    def save_script(self, script_data_instance):
        print("script_data_instance-steps:", str(script_data_instance.steps[0].__dict__))
        encrypted_data = self.encrypt_data(script_data_instance)
        self.script.script_data = encrypted_data
        self.save_script_to_db_versions(encrypted_data)
        self.save_to_file(encrypted_data)


    def save_to_file(self, encrypted_data):
        project_folder = os.path.join(settings.MEDIA_ROOT, 'scripts', f'project_{self.project.id}')
        os.makedirs(project_folder, exist_ok=True)

        file_path = os.path.join(project_folder, f'script_{self.script.id}_{self.script.script_version}.ScriptQ')
        with open(file_path, 'wb') as f:
            f.write(encrypted_data)

    def decrypt_script(self, encrypted_data):
        fernet = Fernet(self.encryption_key)
        return pickle.loads(fernet.decrypt(encrypted_data))

    def load_script_version(self, script_id ,version_number ):
        table_name = f"project_script_versions"
        with self.using_project_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    SELECT script_data FROM {table_name}
                    WHERE script_id = %s AND script_version = %s;
                """, [script_id, version_number])
                row = cursor.fetchone()
                if row:
                    encrypted_data = row[0]
                    return self.decrypt_script(encrypted_data)

        return None


    def get_script_from_db(self, version_number, script_id):

        table_name = f"project_script_versions"
        with self.using_project_db() as connection:
            with connection.cursor() as cursor:
                # Query the database for the specific script version
                cursor.execute(f"""
                    SELECT * FROM {table_name}
                    WHERE script_id = %s AND version_number = %s;
                """, [script_id, version_number])

                row = cursor.fetchone()
                if not row:
                    raise ValueError(
                        f"Script version not found: script_id={script_id}, version_number={version_number}")

                # Parse and return the result
                return {
                    'id': row[0],
                    'script_id': row[1],
                    'version_number': row[2],
                    'created_at': row[3],
                    'script_data': row[4]
                }

    def save_cript_to_db(self):
        with self.using_project_db() as connection:
            with connection.cursor() as cursor:
                table_name = "project_scripts"
                # Check if the script exists
                query_select = f"""
                    SELECT id, script_version FROM {table_name} WHERE script_name = %s;
                """
                cursor.execute(query_select, [self.script.test_name])
                result = cursor.fetchone()
                script_id, script_version = None, None

                if result:
                    # Script exists, update the version
                    script_id, script_version = result
                    script_version += 1
                    query_update = f"""
                        UPDATE {table_name} SET script_version = %s WHERE id = %s;
                    """
                    cursor.execute(query_update, [script_version, script_id])
                    print(f"Updated script '{self.script.test_name}' to version {script_version}.")
                else:
                    # Script does not exist, create a new one with version 1
                    script_version = 1
                    query_insert = f"""
                        INSERT INTO {table_name} (script_name, script_version) VALUES (%s, %s)
                        RETURNING id;
                    """
                    cursor.execute(query_insert, [self.script.test_name, script_version])
                    script_id = cursor.fetchone()[0]
                    print(f"Created script '{self.script.test_name}' with version 1.")

                # Save the script to the versions table
                self.save_script_to_db_versions(self.encrypt_data(self.script), script_id, script_version)

    def save_script_to_db_versions(self, encrypted_data, script_id, script_version):
        table_name = "project_script_versions"
        with self.using_project_db() as connection:
            with connection.cursor() as cursor:
                query_insert = f"""
                    INSERT INTO {table_name} (script_id, script_version, created_at, script_data)
                    VALUES (%s, %s, CURRENT_TIMESTAMP, %s);
                """
                cursor.execute(query_insert, [script_id, script_version, encrypted_data])
                print(f"Saved version {script_version} for script ID {script_id}.")

    def get_script_versions(self,script_id):

        table_name = f"project_script_versions"
        with self.using_project_db() as connection:

            with connection.cursor() as cursor:
                cursor.execute(f"""
                    SELECT script_version, created_at FROM {table_name}
                    WHERE script_id = %s ORDER BY script_version ASC;
                """, [script_id])

                rows = cursor.fetchall()
                versions = [{'version_number': row[0], 'created_at': row[1]} for row in rows]
        return versions