


class ImportCSV:
    @staticmethod
    def reader(file):
        # Read all lines from the file
        lines = file.readlines()
        
        # Iterate through the lines and split by commas
        for line in lines:
            yield line.strip().split(',')
    
    @staticmethod
    def DictReader(file):
        lines = file.readlines()
        headers = lines[0].strip().split(',')
        
        for line in lines[1:]:
            values = line.strip().split(',')
            row_dict = {headers[i]: values[i] for i in range(len(headers))}
            yield row_dict

    @staticmethod
    def writer(file, rows):
        for row in rows:
            file.write(','.join(row) + '\n')
    
    @staticmethod
    def DictWriter(file, fieldnames):
        def writerow(row_dict):
            # Write a row from a dictionary, matching fieldnames order
            row = [str(row_dict.get(field, "")) for field in fieldnames]
            file.write(','.join(row) + '\n')
        return writerow
