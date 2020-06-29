# Create VSI Instances
ibmcloud sl vs create --datacenter=wdc07 --hostname=p100a --domain=brynamo.com --image=2263543 --billing=hourly  --network 1000 --key=1809982 --flavor AC1_16X120X100 --san

ibmcloud sl vs create --datacenter=wdc07 --hostname=p100b --domain=brynamo.com --image=2263543 --billing=hourly  --network 1000 --key=1809982 --flavor AC1_16X120X100 --san

# Prepare the second disk
However, you will still need to log into the Softlayer Portal, find your instances under "devices" and "upgrade" them by adding a second 2 TB SAN drive to each VM, then format the 2TB disk and mount it:

What is it called?
```
ssh -i w251/ssh_key_vsi root@52.117.91.189
```


```
fdisk -l
```

You should see your large disk, something like this
```
Disk /dev/xvdc: 2 TiB, 2147483648000 bytes, 4194304000 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
```
In this case, our disk is called /dev/xvdc. Your disk may be named differently. Format it:
```
# first
mkdir -m 777 /data
mkfs.ext4 /dev/xvdc
```

Add to /etc/fstab
```
# edit /etc/fstab and all this line:
/dev/xvdc /data                   ext4    defaults,noatime        0 0
```
Mount the disk
```
mount /data
```
# Get the VMs set up
1. Login into one of the VMs and use your API key to login into Nvidia Cloud docker registry
2. Pull the latest tensorflow image with python3: docker pull nvcr.io/nvidia/tensorflow:19.05-py3
3. Use the files on `v2/week09/hw/docker/` to create an openseq2seq image
4. Copy the created docker image to the other VM (or repeat the same steps on the other VM)
5. Create containers on both VMs: `docker run --runtime=nvidia -d --name openseq2seq --net=host -e SSH_PORT=4444 -v /data:/data -p 6006:6006 openseq2seq`
6. On each VM, create an interactive bash sesion inside the container: `docker exec -ti openseq2seq bash` and run the following commands in the container shell:
  i. Test mpi: `mpirun -n 2 -H <vm1 private ip address>,<vm2 private ip address> --allow-run-as-root hostname`
  ii. Pull data to be used in neural machine tranlsation training (more info):
  ```
  cd /opt/OpenSeq2Seq
  scripts/get_en_de.sh /data/wmt16_de_en
  ```


# Run Training

```
nohup mpirun --allow-run-as-root -n 4 -H 10.191.251.149:2,10.191.251.161:2 -bind-to none -map-by slot --mca btl_tcp_if_include eth0 -x NCCL_SOCKET_IFNAME=eth0 -x NCCL_DEBUG=INFO -x LD_LIBRARY_PATH python run.py --config_file=/data/transformer-base.py --use_horovod=True --mode=train_eval &
```
