import json
import glob
import os
import sqlite3

conn = sqlite3.connect('CONP.db')
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS exe_records")
cursor.execute("""CREATE TABLE exe_records (

        key_fileHash_pipeline_DOI TEXT PRIMARY KEY,
        pipeline_name TEXT,
        pipeline_DOI TEXT ,
        inFile_name TEXT,
        md5_inFile TEXT,
        prune INTEGER,
        verbose INTEGER,
        exit_code INTEGER,
        error_message TEXT,
        shell_command TEXT,
        stdout TEXT,
        stdrr TEXT,
        output_file TEXT,
        md5_outFile TEXT
        
            )""")
#SQLite does not have a separate Boolean storage class. Instead, Boolean values are stored as integers 0 (false) and 1 (true).
def fill_exeRecord (contents,count):
    try:
        pipeline_name = contents["summary"]["name"]
        print("pipeline name:    " + pipeline_name)
    except KeyError or ValueError or JSONDecodeError:
        pipeline_name = ""
        pass

    try:
        pipeline_DOI = contents["summary"]["descriptor-doi"]
        splited = str(pipeline_DOI)
        splited = splited.split("/")
        pipeline_DOI = splited[1]

        print("pipeline DOI:    " + pipeline_DOI)
    except KeyError or ValueError or JSONDecodeError:
        pipeline_DOI = ""

###################################
    try:
        inFile_name = contents["public-invocation"]["infile"]["file-name"]
        print("inFile name:    " + inFile_name)
    except KeyError or ValueError or JSONDecodeError:
        inFile_name= ""

    try:
        md5_inFile = contents["public-invocation"]["infile"]["md5sum"]
        print("MD5 inFile:    " + md5_inFile)
    except KeyError or ValueError or JSONDecodeError:
        md5_inFile = ""


###################################
    try:
        infile_bvals = contents["public-invocation"]["bvals"]["file-name"]
        print("bvals file name:    " + infile_bvals)
    except KeyError or ValueError or JSONDecodeError:
        infile_bvals = ""
    try:
        md5_bvals = contents["public-invocation"]["bvals"]["md5sum"]
        print("MD5 bvals:    " + md5_bvals)
    except KeyError or ValueError or JSONDecodeError:
        md5_bvals = ""
###################################

    try:
        infile_bvecs = contents["public-invocation"]["bvecs"]["file-name"]
        print("bvecs file name:    " + infile_bvecs)
    except KeyError or ValueError or JSONDecodeError:
        infile_bvecs = ""
    try:
        md5_bvecs = contents["public-invocation"]["bvecs"]["md5sum"]
        print("MD5 bvecs:    " + md5_bvecs)
    except KeyError or ValueError or JSONDecodeError:
        md5_bvecs = ""

###################################
    try:
        infile_diffusion_image = contents["public-invocation"]["diffusion_image"]["file-name"]
        print("diffusion_image file name:    " + infile_diffusion_image)
    except KeyError or ValueError or JSONDecodeError:
        infile_diffusion_image =""
    try:
        md5_diffusion_image = contents["public-invocation"]["diffusion_image"]["md5sum"]
        print("MD5 diffusion_image:    " + md5_diffusion_image)
    except KeyError or ValueError or JSONDecodeError:
        md5_diffusion_image = ""

###################################
    # try:
    #     infile_labels = contents["public-invocation"]["labels"]["file-name"]
    #     print("labels file name:    " + infile_labels)
    # except KeyError or ValueError or JSONDecodeError:
    #     pass
    # try:
    #     md5_labels = contents["public-invocation"]["labels"]["md5sum"]
    #     print("MD5 labels:    " + md5_labels)
    # except KeyError or ValueError or JSONDecodeError:
    #     pass
##################################
    try:
        prune = str(contents["public-invocation"]["prune"])
        print("prune  :    " + str(prune))
    except KeyError or ValueError or JSONDecodeError:
        prune = ""
        ### !!!!! what should we replace if not exists? what is the none value for prone???????????????????????????????????????????????
###################################
    try:
        infile_seed_mask = contents["public-invocation"]["seed_mask"]["file-name"]
        print("seed_mask file name:    " + infile_seed_mask)
    except KeyError or ValueError or JSONDecodeError:
        infile_seed_mask = ""
    try:
        md5_seed_mask = contents["public-invocation"]["seed_mask"]["md5sum"]
        print("MD5 seed_mask:    " + md5_seed_mask)
    except KeyError or ValueError or JSONDecodeError:
        md5_seed_mask = ""
##################################
    try:
        verbose = contents["public-invocation"]["verbose"]
        print("verbose:    " + str(verbose))
    except KeyError or ValueError or JSONDecodeError:
        verbose = 555 # as not defined, I don't know what to insert as noy defined.......???????????????????????????????????????????????????
##################################
    try:
        infile_whitematter_mask = contents["public-invocation"]["whitematter_mask"]["file-name"]
        print("whitematter_mask file name:    " + infile_whitematter_mask)
    except KeyError or ValueError or JSONDecodeError:
        infile_whitematter_mask = ""
    try:
        md5_whitematter_mask = contents["public-invocation"]["whitematter_mask"]["md5sum"]
        print("MD5 whitematter_mask:    " + md5_whitematter_mask)
    except KeyError or ValueError or JSONDecodeError:
        md5_whitematter_mask = ""
    ##################################
    try:
        exit_code = contents["public-output"]["exit-code"]
        print("exit code:    "  + str(exit_code))
    except KeyError or ValueError or JSONDecodeError:
        exit_code = 555  # as not defined, I don't know what to insert as noy defined.......???????????????????????????????????????????????????
##################################
    try:
        error_message = contents["public-output"]["error-message"]
        print("error message:    "  + error_message)
    except KeyError or ValueError or JSONDecodeError:
        error_message = ""
###############################
    try:
        shell_command = contents["public-output"]["shell-command"]
        print("shell_command :    " + shell_command)
    except KeyError or ValueError or JSONDecodeError:
        shell_command = ""
###############################

    try:
        stdout = contents["public-output"]["stdout"]
        print("stdout:    " + str(stdout))
        #ADD the str(stdout) in table
    except KeyError or ValueError or JSONDecodeError:
        stdout = ""
################################
    try:
        stderr = contents["public-output"]["stderr"]
        print("stderr:    " + str(stderr))
    except KeyError or ValueError or JSONDecodeError:
        stderr = ""
################################

    try:
        output_file = contents["public-output"]["output-files"]["outfile"]["file-name"]
        print("output file:     " + output_file)
    except KeyError or ValueError or JSONDecodeError:
        output_file = ""
    try:
        md5_outFile = contents["public-output"]["output-files"]["outfile"]["md5sum"]
        print("MD5 outFile:     " + md5_outFile)
    except KeyError or ValueError or JSONDecodeError:
        md5_outFile =""


####################################

    try:
        output_fibers = contents["public-output"]["output-files"]["fibers"]["file-name"]
        print("output fibers:     " + output_fibers)
    except KeyError or ValueError or JSONDecodeError:
        output_fibers = ""
    try:
        md5_fibers = contents["public-output"]["output-files"]["fibers"]["md5sum"]
        print("MD5 fibers:     " + md5_fibers)
    except KeyError or ValueError or JSONDecodeError:
        md5_fibers = ""


####################################

    try:
        output_graph = contents["public-output"]["output-files"]["graph"]["file-name"]
        print("output graph:     " + output_graph)
    except KeyError or ValueError or JSONDecodeError:
        output_graph =""
    try:
        md5_graph = contents["public-output"]["output-files"]["graph"]["md5sum"]
        print("MD5 graph:     " + md5_graph)
    except KeyError or ValueError or JSONDecodeError:
        md5_graph =""
####################################

    try:
        output_graph_plot = contents["public-output"]["output-files"]["graph_plot"]["file-name"]
        print("output graph_plot:     " + output_graph_plot)
    except KeyError or ValueError or JSONDecodeError:
        output_graph_plot = ""
    try:
        md5_graph_plot = contents["public-output"]["output-files"]["graph_plot"]["md5sum"]
        print("MD5 graph_plot:     " + md5_graph_plot)
    except KeyError or ValueError or JSONDecodeError:
        md5_graph_plot =""

    key_pipeline_DOI_fileHash = str(count)+"---"+md5_inFile+pipeline_DOI
    cursor.execute("INSERT INTO exe_records VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);",(key_pipeline_DOI_fileHash,pipeline_name, pipeline_DOI, inFile_name, md5_inFile,prune,verbose,exit_code,error_message,shell_command,stdout,stderr,output_file,md5_outFile))
    conn.commit()


json_files = [i for i in os.listdir(os.getcwd()+"/exe_records") if i.endswith("json")]
count = 0;
for exeRecord in json_files:

    with open(os.getcwd()+"/exe_records/"+exeRecord) as exeRec:
        contents = json.load(exeRec)
        count = count + 1
        fill_exeRecord(contents,count)



