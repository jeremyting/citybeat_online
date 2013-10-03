from mongodb_interface import MongoDBInterface



def main():
    ec2 = MongoDBInterface()
    ec2.setDB('test_chaolun')
    ec2.setCollection('test')
    print ec2.getAllDocumentIDs()

if __name__ == '__main__':
    main()
