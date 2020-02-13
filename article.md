All about Docker
=============
<img src="https://imgdb.in/gtN7" width="450px" height="300px" title="" alt="RubberDuck"></img><br/>

What is docker
-------------
Docker is a tool designed to make it easier to create, deploy, and run applications by using containers. Containers allow a developer to package up an application with all of the parts it needs, such as libraries and other dependencies, and ship it all out as one package.
Docker is a container-based open source virtualization platform.
> (https://opensource.com/resources/what-docker)

Why use docker
-------------
If you want to install gitlab on your ubuntu server, you have to follow next instructions.

> sudo apt-get update<br/>
> sudo apt-get install -y curl openssh-server ca-certificates<br/>
> sudo apt-get install -y postfix<br/>
> curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ee/script.deb.sh | sudo bash<br/><br/>
> sudo EXTERNAL_URL="http://gitlab.example.com" apt-get install gitlab-ee<br/>

If you CentOS, it is little different.
> sudo yum install -y curl policycoreutils-python openssh-server
> sudo systemctl enable sshd
> sudo systemctl start sshd<br/>
> sudo firewall-cmd --permanent --add-service=http<br/>
> sudo systemctl reload firewalld<br/>
> sudo yum install postfix<br/>
> sudo systemctl enable postfix<br/>
> sudo systemctl start postfix<br/>
> curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ee/script.rpm.sh | sudo bash<br/>
> sudo EXTERNAL_URL="http://gitlab.example.com" yum install -y gitlab-ee<br/>

And depending on the OS and excution environment you use, It change every time.<br/>
But if you use docker, No matter what OS you use you can make your own server by this commands.
> $ docker run --detach \<br/>
>     --hostname gitlab.example.com \<br/>
>     --publish 443:443 --publish 80:80 --publish 22:22 \<br/>
>     --name gitlab \<br/>
>     --restart always \<br/>
>     --volume /srv/gitlab/config:/etc/gitlab \<br/>
>     --volume /srv/gitlab/logs:/var/log/gitlab \<br/>
>     --volume /srv/gitlab/data:/var/opt/gitlab \<br/>
>     gitlab/gitlab-ce:latest<br/>

As you can see, It provides a large number of convenience and scalability

Docker container
-------------
Containers can be thought of as square boxes for cargo transportation on board ships. Each container can hold various cargoes such as clothes, shoes, electronics, alcohol, fruit, etc. can.

Containers that are talked about on the server are similar, and they simplify the deployment and management of programs by abstracting various programs and execution environments into containers and providing the same interface. You can abstract any program such as backend program, database server, message queue, etc. into a container and run it anywhere on the assembly PC, AWS, Azure, Google cloud, etc.

The best company to use containers is Google, and according to the 2014 announcement, Google says that all services act as containers and run 2 billion containers every week.

Docker image
-------------
The most important concept in Docker is the concept of images with containers.

The image contains the files and settings required to run the container and has no state and is immutable. A container can be thought of as running an image, and values added or changed are stored in the container. You can create multiple containers from the same image, and the image remains unchanged even if the state of the container changes or the container is deleted.

The ubuntu image contains all the files needed to run ubuntu, and the MySQL image contains the files, executable commands and port information needed to run MySQL on debian. A more complex example, Gitlab images have ruby, go, database, redis, gitlab source, nginx, etc.

Literally, the image contains all the information needed to run the container, so you no longer need to compile the dependency files and install anything. Now, when a new server is added, all you have to do is download the image you created and create a container. You can run multiple containers on one server, and dozens, hundreds, or even thousands of servers are no problem.

Docker file
-------------
Docker writes the image creation process using its own DSLDomain-specific language in a file called Dockerfile to create the image. Looking at the sample above, you can see that it's not that complicated.

This is a very simple but useful idea. If you have some experience installing a dependency package and creating a configuration file to install a program on your server, you can no longer blog the process or write it down in Notepad and manage it with Dockerfile. This file is versioned with the source and anyone can view and modify the image creation process if desired.


How to install
-------------
> curl -fsSL https://get.docker.com/ | sudo sh

If the installation is complete, enter Docker command to check if the installation is successful.

> docker version

The command to run docker is:
> docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]

Run container
-------------
Create a ubuntu 18.04 container and try to go inside it.
> docker run ubuntu:18.04
If you use the run command, it checks to see if the image you want to use is saved. If not, it downloads and creates and starts a container.

We never downloaded the ubuntu: 18.04 image, so the container ran after downloading the image. The container ran successfully but didn't tell it what to do so the container exits as soon as it is created. Because the container is a process, if no process is running, the container terminates.

Now let's run the ubuntu:18.04 container by typing the command /bin/bash.
> docker run -it ubuntu:18.04 /bin/bash

Voila. In a moment Ubuntu was made into a container. Now you can do various things in the newly created Ubuntu container.
Similarly, you can easily create, run, and deploy any program you want, such as MySQL, Redis, tensorflow, into a container.

Docker basic commands
-------------
The command to check the list of containers is:
> docker ps [OPTIONS]

The command to stop a running container is:
> docker stop [OPTIONS] CONTAINER [CONTAINER ...]

The command to completely remove a terminated container is:
> docker rm [OPTIONS] CONTAINER [CONTAINER ...]

The command to view the list of images downloaded by Docker is:
> docker images [OPTIONS] [REPOSITORY [: TAG]]

The command to download an image is:
> docker pull [OPTIONS] NAME [: TAG | @DIGEST]

Here's how to delete an image:
> docker rmi [OPTIONS] IMAGE [IMAGE ...]

A good way to verify that the container is working is to check the logs. Here's how to check the log:
> docker logs [OPTIONS] CONTAINER

Here's how to run a container command:
> docker exec [OPTIONS] CONTAINER COMMAND [ARG ...]
