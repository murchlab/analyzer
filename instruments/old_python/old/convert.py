import os


def txt2csv(filename, in_dir=os.getcwd(), out_dir=os.getcwd()):
    # Takes file with list of numbers and rewrites as list of (index, number)

    # should do error checking, but whatevs
    all_lines= open(in_dir+filename, 'r').readlines()
    if out_dir[-1] != "\\":
        out_dir +="\\"

    new_file_name = filename[:-4] + '.csv'

    print "Writing file to", out_dir+new_file_name
    with open(out_dir+new_file_name,'w') as open_file:
        for i,line in enumerate(all_lines):
              open_file.write("{0}, {1}".format(i,line) )

        if False and filename == "11ptcsvtest_ch1_10.csv":   
            for (i,line) in zip(range(len(all_lines)), all_lines)[3980:4000]: 
                print i, line              

#END txt2csv            
    
    

if __name__ == '__main__':

    in_path = "C:\\arbtests\\test6\\csv\\"
    out_path = "C:\\arbtests\\test6\\csv2\\"
    for filename in os.listdir(in_path):
        if filename.endswith('.csv'):
            print "rewriting", filename
            txt2csv(filename, in_dir=in_path, out_dir=out_path)
    
