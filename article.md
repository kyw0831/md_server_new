All about Docker
=============

What is docker
-------------
Docker is a tool designed to make it easier to create, deploy, and run applications by using containers. Containers allow a developer to package up an application with all of the parts it needs, such as libraries and other dependencies, and ship it all out as one package.
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
> sudo yum install -y curl policycoreutils-python openssh-server<br/>
> sudo systemctl enable sshd<br/>
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


How to use
-------------

Managing containers in real project
-------------

Docker file
-------------

Docker compose file
-------------
