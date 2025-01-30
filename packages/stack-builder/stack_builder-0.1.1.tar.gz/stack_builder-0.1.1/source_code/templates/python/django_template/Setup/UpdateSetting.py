import re

class UpdateSetting:
    @staticmethod
    def update_database_config(setting_template_path, setting_output_path):
        """
        Updates the database configuration in the settings file.

        Args:
            setting_template_path (str): Path to the database template file.
            setting_output_path (str): Path to the output settings file to be updated.

        Returns:
            str: A message indicating the success of the operation.

        Raises:
            Exception: If an error occurs during the update process.
        """
        try:
            # Read the contents of the current settings file
            with open(setting_output_path, 'r') as setting_output:
                setting_output_contents = setting_output.read()

            # Read the contents of the database template file
            with open(setting_template_path, 'r') as setting_template:
                setting_template_contents = setting_template.read()


            # Pattern to match the existing DATABASES configuration block
            database_pattern = r"DATABASES\s*=\s*\{(?:[^{}]|\{[^{}]*\})*\}\s*"

            # Replace the existing DATABASES block with the new template content
            updated_setting = re.sub(
                database_pattern,
                setting_template_contents,
                setting_output_contents,
                flags=re.DOTALL
            )

            # Write the updated configuration back to the settings file
            with open(setting_output_path, 'w') as setting_output:
                setting_output.write(updated_setting)

            return "Database configuration update was successful."
        
        except Exception as e:
            # Print an error message if an exception occurs
            print(f"Error occurred while updating settings: {e}")
