import os
import sys

def main():
    if len(sys.argv)!=4:
        sys.stderr.write("Usage: python %s launch/kill gp/api host_list_file \n\n"%sys.argv[0])
        raise SystemExit(1)
    
    lines = open(sys.argv[3]).readlines()
    for line in lines:
        if sys.argv[1]=='launch':
            if sys.argv[2]=='api': 
                launch_cmd = "ssh kx19@"+ line[:-1] + " \"source ~/virtual_env/virtualenv-1.9.1/new_env/bin/activate; nohup python /grad/users/kx19/citybeat_smil/citybeat/crawlers/instagram/run_api_worker.py > /.freespace/api_worker_log.txt < /dev/null 2>&1 &\"";
            elif sys.argv[2]=='gp':
                launch_cmd = "ssh kx19@"+ line[:-1] + " \"source ~/virtual_env/virtualenv-1.9.1/new_env/bin/activate; nohup python /grad/users/kx19/citybeat_smil/citybeat/crawlers/instagram/run_gp_worker.py > /.freespace/gp_worker_log.txt < /dev/null 2>&1 &\"";
            os.popen(launch_cmd)
        elif sys.argv[1]=='kill':
            if sys.argv[2]=='api':
                kill_cmd = " \"kill -9 \$(ps -ef|grep kx19|grep run_api_worker|grep -v grep |  awk '{print \$2}')\"";
            elif sys.argv[2]=='gp':
                kill_cmd = " \"kill -9 \$(ps -ef|grep kx19|grep run_gp_worker| grep -v grep|  awk '{print \$2}')\"";
            ssh_prefix = "ssh kx19@"+line[:-1];
            os.popen(ssh_prefix+kill_cmd)

if __name__ == "__main__":
    main()
