resource_types = [
                ('Audiovisual', 'Audiovisual'), 
                ('Book', 'Book'), 
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
        with open("tags.pickle", "rb") as file:
                custom_tags = pickle.load(file)     
                return custom_tags