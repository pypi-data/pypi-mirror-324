import os
from cryptography.fernet import Fernet
from django.conf import settings
from django.core.management import call_command
from django.db import connections


class Project_db_creator:

    def db_check_sqlite_existence(self, project_id):
        """
        Check if the SQLite database for the given project exists.
        """
        project_id = str(project_id) + ".sqlite3"
        db_path = os.path.join(settings.BASE_DIR, project_id)

        if os.path.exists(db_path):
            print(f"Database '{project_id}' already exists.")
            return False
        else:
            return True

    def db_create_project_new_sqlite_db(self, project_id):
        """
        Create a new SQLite database for a project, configure it in Django settings,
        and apply migrations to initialize the schema.
        """
        project_id = str(project_id)  # Ensure project_id is a string
        db_path = os.path.join(settings.BASE_DIR, f'{project_id}.sqlite3')

        # Default database configuration for the project
        default_db_config = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': db_path,
            'TIME_ZONE': settings.TIME_ZONE,
            'CONN_MAX_AGE': 0,
            'OPTIONS': {},
            'AUTOCOMMIT': True,
            'CONN_HEALTH_CHECKS': False,
            'ATOMIC_REQUESTS': False,
        }

        # Add the new database configuration to settings.DATABASES if not present
        if project_id not in settings.DATABASES:
            print(f"Before update: {settings.DATABASES}")
            settings.DATABASES[project_id] = default_db_config
            print(f"After update: {settings.DATABASES}")
            self.persist_to_settings_file(project_id, default_db_config)
        # Ensure the database is created and connected
        try:
            with connections[project_id].cursor() as cursor:
                pass  # This ensures the database file is created
            print(f"Database '{project_id}' created successfully at {db_path}.")
        except Exception as e:
            print(f"Error creating database '{project_id}': {e}")
            return

        # Run migrations to apply the schema

        try:
            # Identify apps to migrate
            excluded_apps = ['auth', 'contenttypes', 'admin', 'sessions','messages','staticfiles']
            apps_to_migrate = [
                app_label.split('.')[-1] for app_label in settings.INSTALLED_APPS
                if app_label.split('.')[-1] not in excluded_apps
            ]

            # Apply migrations for each app
            for app_label in apps_to_migrate:
                call_command('migrate', app_label=app_label, database=project_id, interactive=False)

            print(f"Migrations applied successfully for database '{project_id}'.")
        except Exception as e:
            print(f"Error applying migrations for database '{project_id}': {e}")

    def persist_to_settings_file(self, project_id, config):
        """
        Persist the database configuration directly to the settings.py file.
        """
        settings_path = os.path.join(settings.BASE_DIR, "script_creator", "settings.py")

        with open(settings_path, "r") as file:
            lines = file.readlines()

        inside_databases = False
        for i, line in enumerate(lines):
            if line.strip().startswith("DATABASES = {"):
                inside_databases = True
            if inside_databases and line.strip() == "}":  # End of DATABASES dictionary
                break
        else:
            raise ValueError("DATABASES dictionary not found in settings.py")

        # Prepare the configuration string
        config_str = f"\n    '{project_id}': {config},\n"

        # Check if the project_id already exists in DATABASES
        for j in range(i + 1, len(lines)):
            if f"'{project_id}':" in lines[j]:
                print(f"Project ID '{project_id}' already exists in settings.py. Skipping.")
                return

        # Insert the new configuration before the closing brace of the DATABASES dictionary
        for j in range(i + 1, len(lines)):
            if lines[j].strip() == "}":  # End of DATABASES dictionary
                lines.insert(j, config_str)
                break

        # Write the updated settings back to the file
        with open(settings_path, "w") as file:
            file.writelines(lines)

        print(f"Persisted database configuration for project '{project_id}' to settings.py.")

    def db_create_encryption_key(self, project_id, name):
        project_id = str(project_id)

        encryption_key = Fernet.generate_key()

        with connections[project_id].cursor() as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS encryption_keys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    encryption_key BLOB NOT NULL
                );
            """)


            cursor.execute(f"""
                INSERT INTO encryption_keys (project_id, name, encryption_key)
                VALUES (%s, %s, %s);
            """, [project_id, name, encryption_key])

        print(f"Encryption key created and stored for project {project_id} with name '{name}'.")

    def db_create_project_table_script_versions(self, project_id):
        """
        Create the table for script versions in the project's database.
        """
        project_id = str(project_id)
        print("Project ID:", project_id)

        table_name = "project_script_versions"
        with connections[project_id].cursor() as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    script_id INTEGER NOT NULL,
                    script_version INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    script_data BLOB,
                    FOREIGN KEY (script_id) REFERENCES project_scripts(id) ON DELETE CASCADE
                );
            """)

    def db_create_project_table_scripts(self, project_id):
        """
        Create the table for scripts in the project's database.
        """
        project_id = str(project_id)
        print("Project ID:", project_id)

        table_name = "project_scripts"
        with connections[project_id].cursor() as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    script_name TEXT NOT NULL, 
                    script_version INTEGER NOT NULL
                );
            """)

        print(f"Table '{table_name}' created successfully in database '{project_id}'.")
