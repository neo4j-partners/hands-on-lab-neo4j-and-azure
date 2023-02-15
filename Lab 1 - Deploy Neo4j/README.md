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

Password should be 12 characters or longer.  
My go to throw away password is "Foo12345678!"

![](images/02-configure.png)

Go to the `Neo4j Config` tab to configure the Graph Data Platform

Let's leave the Virtual Machine Size as-is

For the "Node Count" select "1." This is the number of Neo4j nodes that will be deployed in the autoscaling group.  Because we're using GDS, we want a single node.  If we were using only GDB, we might deploy in a 3 node cluster for resilience.

Leave the Disk Size to the default. 
**But ensure that the Graph Database version selected is 5**

Select `True` to Install Graph Data Science.

Graph Database Enterprise does not require a license key.  Graph Data Science Enterprise does need a license key.  If you don't specify it, Graph Data Science will start in Community mode.  That means it will not have some features we're going to use later in the lab.  Bloom requires a license key and will not allow you to login without one.  You can use these license keys:

graphDataScienceLicenseKey: 

    eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRvZGRhd3NAYW1hem9uLmNvbSIsImV4cCI6MTY4NDA4MDAwMCwiZmVhdHVyZVZlcnNpb24iOiIqIiwib3JnIjoiQW1hem9uIFdlYiBTZXJ2aWNlcywgSW5jLiAoQVdTKSAoUGFydG5lcikiLCJwdWIiOiJuZW80ai5jb20iLCJxdWFudGl0eSI6IjEiLCJyZWciOiJUb2RkIEhlYXRoIiwic2NvcGUiOiJUcmlhbCIsInN1YiI6Im5lbzRqLWdkcyIsInZlciI6IioiLCJpc3MiOiJuZW80ai5jb20iLCJuYmYiOjE2NzY0NzA1MzAsImlhdCI6MTY3NjQ3MDUzMCwianRpIjoiMzNQZlVIbmxuIn0.cepKxiXRKUGlqudX_bQCxYm94QVn0eSvG3eu6KEaVcZXhkQSU4HfJTtZT_ZJJVSj7XZOaLEGlAZDD4_ccP6ZK6ICjj-wADDwyGwj7dtM6yX-bESunV0f4rIY8ELxoYFdbgI-Xk4ldltHsJTqKXOci4w7lRrcxc9tB1PK4BhSCalHvglo4G_UtkAuzNerjfbKNAxZhL6T_hHrf4pAAXYOAZRtJinhxBJAdbJ9oaXTdpwDmTokFkkQlfnyPUfILWA2SiY2Hagns-5Npax4RXGhniEgmYLkW_wWZVH4khwuezISbda5VCUfOAzbXBXnXiFBcSjBvLhZy-JFmmihDAPnGw

Select `True` to Install Bloom.

bloomLicenseKey:

    eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRvZGRhd3NAYW1hem9uLmNvbSIsImV4cCI6MTY4NDA4MDAwMCwiZmVhdHVyZVZlcnNpb24iOiIqIiwib3JnIjoiQW1hem9uIFdlYiBTZXJ2aWNlcywgSW5jLiAoQVdTKSAoUGFydG5lcikiLCJwdWIiOiJuZW80ai5jb20iLCJxdWFudGl0eSI6IjEiLCJyZWciOiJUb2RkIEhlYXRoIiwic2NvcGUiOiJUcmlhbCIsInN1YiI6Im5lbzRqLWJsb29tLXNlcnZlciIsInZlciI6IioiLCJpc3MiOiJuZW80ai5jb20iLCJuYmYiOjE2NzY0NzAzMjAsImlhdCI6MTY3NjQ3MDMyMCwianRpIjoiZzZXYjRoY0lWIn0.tfh2MXlPuo4ICH1ODhD1N1uzLEYSqUB3lPbiX4PCuJut9xm-BuMqpeNEDjO-yuc_LyT7NqTyvYAaHbuKtz7L8WNDNusSmgKhiJDsnff8zyqT_qUlAaj79gSRC24id1wONhedfEyr0axgKC92tXRaCfG8XdEGQE0kNIWIeEfcBTnNWfcS00CdoqJlxdbE2Z8zmBngCea6vWsY_7VELs0ZiZX9Q57VxuwHs19vL1l6hbGQuDLVAuCmR5o1Lw6_8vN1ymCmYtrfu0W1ipyZlcVOIH4OmZfIhojsXfomIwZEvAdKQyC29a4Ymi3a7QaVlE2cDWrdzvOF6EKaEudjmEoWRQ


With all that config specified, it's time to click the "Review + Create" button.

Review the configurations and click "Create" button

![](images/03-neo4j-config.png)


When all done, you'll be taken to the "Deployments" page.

![](images/04-complete.png)

You will see the nodes, vnet, NSG and deployments under "Deployment Details" section

Once the deployment is completed, click on "Outputs" in the left. Copy the URI for the Neo4j Browser.  You're going to need that in the next lab.

![](images/05-output.png)

You're now all ready for the next lab where we're going to start using the Neo4j deployment we just created.
