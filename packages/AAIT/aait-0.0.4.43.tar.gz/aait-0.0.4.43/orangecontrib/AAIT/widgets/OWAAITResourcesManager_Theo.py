import os
import sys

from AnyQt import QtWidgets
from AnyQt.QtCore import QTimer
from AnyQt.QtWidgets import QApplication  # QMainWindow, QFileDialog
from AnyQt.QtWidgets import (QComboBox, QDialog, QGroupBox, QHBoxLayout,
                             QLabel, QPushButton, QTextEdit, QVBoxLayout)
from Orange.widgets import widget

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.fix_torch import fix_torch_dll_error
    from Orange.widgets.orangecontrib.AAIT.utils import (MetManagement,
                                                         SimpleDialogQt)
    from Orange.widgets.orangecontrib.AAIT.utils.MetManagement import (
        GetFromRemote, get_aait_store_requirements_json)
    from Orange.widgets.orangecontrib.AAIT.utils.initialize_from_ini import apply_modification_from_python_file
else:
    from orangecontrib.AAIT.fix_torch import fix_torch_dll_error
    from orangecontrib.AAIT.utils import (MetManagement,
                                                         SimpleDialogQt)
    from orangecontrib.AAIT.utils.MetManagement import (
        GetFromRemote, get_aait_store_requirements_json)
    from orangecontrib.AAIT.utils.initialize_from_ini import apply_modification_from_python_file
fix_torch_dll_error.fix_error_torch()

@apply_modification_from_python_file(filepath_original_widget=__file__)
class OWAAITResourcesManager(widget.OWWidget):
    name = "AAIT Resources Manager Multi Repo"
    description = "Manage AAIT resources, such as model, example workflows, datasets...."
    icon = "icons/documents.png"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/documents.png"
    priority = 1001
    # Path
    dossier_du_script = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        super().__init__()
        self.requirements = []  # Changed to list to store multiple repositories' requirements
        self.current_repositories = []  # Store paths of selected repositories
        self.controlAreaVisible = False

    # trigger if standard windows is opened
    def showEvent(self, event):
        super().showEvent(event)
        self.show_dialog()
        # We cannot close the standard ui widget it is displayed
        # so it makes a little tinkles :(
        QTimer.singleShot(0, self.close)

    def show_dialog(self):
        # third-party code execution vs standard code execution
        if False == os.path.isfile(MetManagement.get_local_store_path() + "AddOn/prefix_show_dialog.py"):
            dialog = QDialog()
            layout_a = QVBoxLayout()
            dialog.setLayout(layout_a)
            model = None
        else:
            sys.path.append(MetManagement.get_local_store_path() + "AddOn")
            import prefix_show_dialog
            stable_dependency = True
            if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
                stable_dependency = False
            dialog, model = prefix_show_dialog.prefix_dialog_function(self,stable_dependency)

        # download section
        main_layout = QVBoxLayout()
        group_box = QGroupBox("Download new minimum working example")
        group_layout = QVBoxLayout()

        # Elements are presented horizontally
        h_layout = QHBoxLayout()
        v_layout_button_combo_box = QVBoxLayout()
        self.comboBox = QComboBox()
        self.comboBox.setMinimumSize(200, 10)
        
        # Add repository management section
        repo_layout = QHBoxLayout()
        self.repo_combo = QComboBox()
        self.repo_combo.setMinimumSize(200, 10)
        self.ressource_path_button = QPushButton('Add repository')
        self.remove_repo_button = QPushButton('Remove repository')
        
        repo_layout.addWidget(self.repo_combo)
        repo_layout.addWidget(self.ressource_path_button)
        repo_layout.addWidget(self.remove_repo_button)
        
        v_layout_button_combo_box.addLayout(repo_layout)
        verticalSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        v_layout_button_combo_box.addItem(verticalSpacer)
        v_layout_button_combo_box.addWidget(self.comboBox)
        self.saveButton = QPushButton('Download')
        self.label_info = QLabel('')
        v_layout_button_combo_box.addWidget(self.saveButton)
        v_layout_button_combo_box.addWidget(self.label_info)

        # Add v_layout_button_combo_box to h_layout
        h_layout.addLayout(v_layout_button_combo_box)
        
        # Add h_layout to group_layout
        group_layout.addLayout(h_layout)
        group_box.setLayout(group_layout)
        main_layout.addWidget(group_box)
        main_layout.setContentsMargins(5, 5, 5, 5)
        dialog.layout().insertLayout(0, main_layout)

        # Connect signals
        self.comboBox.currentIndexChanged.connect(self.handleComboBoxChange)
        self.saveButton.clicked.connect(self.saveFile)
        self.remove_repo_button.clicked.connect(self.remove_repository)
        self.repo_combo.currentIndexChanged.connect(self.handle_repository_change)
        self.ressource_path_button.clicked.connect(self.update_ressource_path)
        
        # Initialize repositories
        self.load_repositories()

        if False == os.path.isfile(MetManagement.get_local_store_path() + "AddOn/postfix_show_dialog.py"):
            dialog.exec()
        else:
            sys.path.append(MetManagement.get_local_store_path() + "AddOn")
            import postfix_show_dialog
            stable_dependency = True
            if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
                stable_dependency = False
            postfix_show_dialog.postfix_dialog_function(dialog, model)

    def load_repositories(self):
        """Load saved repositories from settings"""
        default_repo = MetManagement.get_aait_store_remote_ressources_path()
        if default_repo and default_repo not in self.current_repositories:
            self.current_repositories.append(default_repo)
        
        self.repo_combo.clear()
        self.repo_combo.addItems(self.current_repositories)
        self.update_requirements()

    def update_requirements(self):
        """Update requirements from all repositories"""
        self.requirements = []
        for repo in self.current_repositories:
            MetManagement.set_aait_store_remote_ressources_path(repo)
            repo_requirements = get_aait_store_requirements_json()
            if repo_requirements:
                # Add repository information to each requirement
                for req in repo_requirements:
                    req['repository'] = repo
                self.requirements.extend(repo_requirements)
        self.populate_combo_box()

    def handle_repository_change(self, index):
        """Handle repository selection change"""
        if index >= 0:
            selected_repo = self.current_repositories[index]
            MetManagement.set_aait_store_remote_ressources_path(selected_repo)

    def remove_repository(self):
        """Remove currently selected repository"""
        current_index = self.repo_combo.currentIndex()
        if current_index >= 0:
            self.current_repositories.pop(current_index)
            self.repo_combo.removeItem(current_index)
            self.update_requirements()

    def populate_combo_box(self):
        # clean combo box if we change of repository
        self.comboBox.clear()
        workflows = []
        descriptions = dict()
        if not self.requirements:
            return
        for element in self.requirements:
            name = f"{element['name']} ({os.path.basename(element['repository'])})"
            workflows.append(name)
            descriptions[name] = element["description"][0]
        self.descriptions = descriptions
        self.comboBox.addItems(workflows)

    def handleComboBoxChange(self, index):
        selected_file = self.comboBox.itemText(index)
        if selected_file=="":
            return
       

    def read_description(self, file_name):
        # Chemin du fichier texte contenant la description
        description_file_path = os.path.join(self.dossier_du_script, 'ows_example',
                                             f'{os.path.splitext(file_name)[0]}.txt')
        # Lire le contenu du fichier s'il existe, sinon retourner une chaîne vide
        if os.path.exists(description_file_path):
            with open(description_file_path, 'r') as file:
                description = file.read()
        else:
            description = ""
        return description

    def saveFile(self):
        # Get selected file and remove repository info from display name
        selected_display = self.comboBox.currentText()
        
        # Find the corresponding requirement
        selected_requirement = None
        for req in self.requirements:
            display_name = f"{req['name']} ({os.path.basename(req['repository'])})"
            if display_name == selected_display:
                selected_requirement = req
                break
        
        if selected_requirement:
            self.label_info.setText('Synchronization in progress')
            QApplication.processEvents()  # Update UI
            
            # Set the correct repository for download
            MetManagement.set_aait_store_remote_ressources_path(selected_requirement['repository'])
            
            # Get just the name without repository info
            file_name = selected_requirement['name']
            
            try:
                # Call GetFromRemote with the local store path as target
                target_path = MetManagement.get_local_store_path()
                GetFromRemote(file_name)
                self.label_info.setText('Download completed')
            except Exception as e:
                self.label_info.setText(f'Error: {str(e)}')
            finally:
                QApplication.processEvents()  # Update UI

    def update_ressource_path(self):
        folder = MetManagement.get_aait_store_remote_ressources_path()
        file = SimpleDialogQt.BoxSelectExistingFile(self, default_dir=folder, extention="Aiit file (*.aait)")
        if file == "":
            return
        if MetManagement.get_size(file) == 0:
            folder = os.path.dirname(os.path.abspath(file)).replace("\\", "/")
            if folder == "":
                return
            if folder[-1] != "/":
                folder += "/"
            if folder not in self.current_repositories:
                self.current_repositories.append(folder)
                self.repo_combo.addItem(folder)
        else:
            # compressed case
            file = file.replace("\\", "/")
            if file not in self.current_repositories:
                self.current_repositories.append(file)
                self.repo_combo.addItem(file)
        
        self.update_requirements()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = OWAAITResourcesManager()
    window.show()
    app.exec_()
