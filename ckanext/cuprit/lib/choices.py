import os
import pickle

resource_types = [
                ('Audiovisual', 'Audiovisual'), 
                ('Book', 'Book'), 
                ('BookChapter', 'BookChapter'),
                ('Booklet', 'Booklet'), 
                ('Collection', 'Collection'),
                ('Computational Notebook', 'Computational Notebook'),
                ('Conference Paper', 'Conference Paper'),
                ('Conference Proceeding', 'Conference Proceeding'),
                ('DataPaper', 'Data Paper'),
                ('Dataset', 'Dataset'),
                ('Dissertation', 'Dissertation'),
                ('Event', 'Event'),
                ('Image', 'Image'),
                ('Interactive Resource', 'Interactive Resource'),
                ('Journal', 'Journal'),
                ('Journal Article', 'Journal Article'),
                ('Model', 'Model'),
                ('Output ManagementPlan', 'Output ManagementPlan'),
                ('Peer Review', 'Peer Review'),
                ('Physical Object', 'Physical Object'),
                ('Preprint', 'Preprint'),
                ('Report', 'Report'),
                ('Service', 'Service'),
                ('Software', 'Software'),
                ('Sound', 'Sound'),
                ('Standard', 'Standard'),
                ('Text', 'Text'),
                ('Workflow', 'Workflow'),
                ('Other', 'Other')
                ] 

def get_custom_tags():
        # get current directory
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # get custom tags
        custom_tags_file = os.path.join(current_dir, 'tags.pickle')
        with open(custom_tags_file, "rb") as file:
                custom_tags = pickle.load(file)     
                return custom_tags