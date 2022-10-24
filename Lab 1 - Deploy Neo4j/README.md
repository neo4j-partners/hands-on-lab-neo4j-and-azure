# Lab 1 - Deploy Neo4j
In this lab, we're going to deploy Neo4j Enterprise Edition from the Azure Marketplace.

## Deploy Neo4j Enterprise Edition through the Marketplace
Let's go to [Azure Marketplace](https://portal.azure.com/#create/hub) search `Neo4j Enterprise Edition`

Neo4j Enterprise Edition is the installable version of Neo4j that runs on Infrastructure as a Service (IaaS).  You have the options to deploy Neo4j Graph Database, Neo4j Graph Data Science and Neo4j Bloom.

* Graph Database is, as the name implies, Neo4j's core database.  It's designed from the ground up to store graphs.  This comes in both a community and an enterprise version.  We're going to use the enterprise version.
* Graph Data Science (GDS) is the graph library that installs on top of the database.  It has implentations of 70 different graph algorithms.  We're going to use GDS to do things like create graph embeddings later in the labs.
* Bloom is a business intelligence tool designed specifically for visualing graphs.  We'll install it as well and use it to explore the data.

Feel free to poke around the listing.

So, let's get started deploying...  
Select BYOL (Bring Your Own License) Plan and then Click on "Create"

![](images/01-sellerprofile.png)

That takes you to a configuration page.  Select the Subscription and Resource Group.
You need to have an empty Resource Group or create a New one.
Provide other needed configurations.

Password should be six characters or longer.  
My go to throw away password is "foo123"

![](images/02-configure.png)

Go to the `Neo4j Config` tab to configure the Graph Data Platform

Let's leave the Virtual Machine Size as-is

For the "Node Count" select "1." This is the number of Neo4j nodes that will be deployed in the autoscaling group.  Because we're using GDS, we want a single node.  If we were using only GDB, we might deploy in a 3 node cluster for resilience.

Leave the Disk Size and Graph Database version to the default.

Select `True` to Install Graph Data Science.

Graph Database Enterprise does not require a license key.  Graph Data Science Enterprise does need a license key.  If you don't specify it, Graph Data Science will start in Community mode.  That means it will not have some features we're going to use later in the lab.  Bloom requires a license key and will not allow you to login without one.  You can use these license keys:

graphDataScienceLicenseKey: 

    eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImJlbkBuZW80ai5jb20iLCJleHAiOjE2NzI1NjAwMDAsImZlYXR1cmVWZXJzaW9uIjoiKiIsIm9yZyI6Ik5lbzRqIFRyYWluaW5nIiwicHViIjoibmVvNGouY29tIiwicXVhbnRpdHkiOiIxIiwicmVnIjoiQmVuIExhY2tleSIsInNjb3BlIjoiUHJvZHVjdGlvbiIsInN1YiI6Im5lbzRqLWdkcyIsInZlciI6IioiLCJpc3MiOiJuZW80ai5jb20iLCJuYmYiOjE2NjQ3Mjc0MDUsImlhdCI6MTY2NDcyNzQwNSwianRpIjoibXI4Vy1RcmVRIn0.FtlakHWD7x2Sn4EmWMwzRnTMsEjsFe9i5JuxlXByfq7WwuGMSbnHxYJK0yCrUfjRkfOkvKsvnEZyQ-H3fxrBZJ1-T0g33LCEWYlfiPY_TOc8qmW1ZbYb4T-dHw8d8RWeNMEAxjwkc7rXBFsnPTvOQqDNY2Fnau7BEwZyKdnLS61e8frhIt2-7abxHHscZcxnXuS6bwybghgetNjeIBYz59rGSN0ovlpmgm00C5egM0F11ntwp5PErWOU-dSTJgmiF_tyO21AHDgGiMpYhUEOM28C4M4gR8a1vpymqRyXCb398teIs6N-CwNygY9ZwW0Aoyj8Ug-Prp-qU29m74fIiA

Select `True` to Install Bloom.

bloomLicenseKey:

    eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImJlbkBuZW80ai5jb20iLCJleHAiOjE2NzI1NjAwMDAsImZlYXR1cmVWZXJzaW9uIjoiKiIsIm9yZyI6Ik5lbzRqIFRyYWluaW5nIiwicHViIjoibmVvNGouY29tIiwicXVhbnRpdHkiOiIxIiwicmVnIjoiQmVuIExhY2tleSIsInNjb3BlIjoiUHJvZHVjdGlvbiIsInN1YiI6Im5lbzRqLWJsb29tLXNlcnZlciIsInZlciI6IioiLCJpc3MiOiJuZW80ai5jb20iLCJuYmYiOjE2NjQ3MjczNzAsImlhdCI6MTY2NDcyNzM3MCwianRpIjoiekw1SV91RlctIn0.NR6hbGT1bfq96ZuOrFtfo2bEB8m8I6eJ9loS2MZr1XMcAyRQPjS9LxPyyORytiJ8_4EJwBjfHpz2rp18zzQV07I3M1wh7Ozj54HHXDF-jkzBjk2Iv4fenJpRoiVfp6AMUiKR2bTwLJog4o6HuBXI2EI-3enGBT7CTFfb7eGKaEUcmAtxR5AZwROr5EOnnJlZqJ0XsCSPIdoHAqIikEZg-gecHssvlB_ryFCAgdJD9jJQDx4ncBP53tYKGVGP8q1nL3UhpoRgAgIXFYBeKmHZKDGKHbB1sgDiq2j-7RWDIyNoRO_8t3YZ7wtTrHcsmz6HUpJECMfV1gLm_o9_TxSW_w


With all that config specified, it's time to click the "Review + Create" button.

Review the configurations and click "Create" button

![](images/03-neo4j-config.png)


When all done, you'll be taken to the "Deployments" page.

![](images/04-complete.png)

You will see the nodes, vnet, NSG and deployments under "Deployment Details" section

Once the deployment is completed, click on "Outputs" in the left. Copy the URI for the Neo4j Browser.  You're going to need that in the next lab.

![](images/05-output.png)

You're now all ready for the next lab where we're going to start using the Neo4j deployment we just created.
