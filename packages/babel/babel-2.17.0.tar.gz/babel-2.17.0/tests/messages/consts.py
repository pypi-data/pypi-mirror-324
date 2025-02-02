import os

TEST_PROJECT_DISTRIBUTION_DATA = {
    "name": "TestProject",
    "version": "0.1",
    "packages": ["project"],
}
this_dir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(this_dir, 'data')
project_dir = os.path.join(data_dir, 'project')
i18n_dir = os.path.join(project_dir, 'i18n')
pot_file = os.path.join(i18n_dir, 'temp.pot')
