# Lab 1 - Deploy Neo4j
In this lab, we're going to deploy Neo4j Enterprise Edition from the Azure Marketplace.

## Deploy Neo4j Enterprise Edition through the Marketplace
First off, let's go to the [Azure Marketplace](https://azuremarketplace.microsoft.com/).

Enter "neo4j" in the search bar and press enter.

![](images/01.png)

You'll see a variety of results.  Some are "By Neo4j."  That means they're official listings published by Neo4j.  Others are from companies like Bitnami who take the community versions of software like Neo4j and publish them themselves.

Neo4j has three listings:

* Neo4j Aura - Our SaaS.  This is currently only available through Azure Marketplace as an annual license, so won't work well for this lab.
* Neo4j Community Edition - This is the free and fully open source version of Neo4j.  It's a great way to get started but is missing some features we'd like to use in the lab.
* Neo4j Enterprise Edition - The commercial version of our self managed, installable product.

We're going to use Neo4j Enterprise Edition for this lab.  Click on that listing.

![](images/02.png)

Neo4j Enterprise Edition is the installable version of Neo4j that runs on Infrastructure as a Service (IaaS).  You have the options to deploy Neo4j Graph Database, Neo4j Graph Data Science and Neo4j Bloom.

* Graph Database is, as the name implies, Neo4j's core database.  It's designed from the ground up to store graphs.  This comes in both a community and an enterprise version.  We're going to use the enterprise version.
* Graph Data Science (GDS) is the graph library that installs on top of the database.  It has implentations of 70 different graph algorithms.  We're going to use GDS to do things like create graph embeddings later in the labs.
* Bloom is a business intelligence tool designed specifically for visualing graphs.  We'll install it as well and use it to explore the data.

Feel free to poke around the listing.  When you're ready to deploy, click "Get It Now."

![](images/03.png)

You may be asked to complete a profile before you can continue.  If so, do that and click "Continue."

![](images/04.png)

You'll then be passed through a series of redirects.

![](images/05.png)

When done, you're at the authenticated marketplace page.  Leave the plan as "BYOL" and click "Create."

![](images/06.png)

Now we need to enter a few values.

* Resource Group - Select the existing resource group in your subscription.
* Region - Select Australia East
* Password - The password should be 12 characters or longer.  A possible throw away password is "Foo12345678!"

Now click "Next."

![](images/07.png)

In this menu we configure our Neo4j EE deployment.  Enter the following values.

* Virtual Machine Size - 1x Standard E4s v5
* Node Count - 1.  More nodes would allow for high availability.
* Disk Size - 32GB
* Graph Database Version - 5.  The other option is a previous version.
* License Type - Enterprise
* Install Graph Data Science - Yes
* Graph Data Science License Key - Be sure to replace "None," don't just paste behind it.

        eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRvZGRhd3NAYW1hem9uLmNvbSIsImV4cCI6MTY4NDA4MDAwMCwiZmVhdHVyZVZlcnNpb24iOiIqIiwib3JnIjoiQW1hem9uIFdlYiBTZXJ2aWNlcywgSW5jLiAoQVdTKSAoUGFydG5lcikiLCJwdWIiOiJuZW80ai5jb20iLCJxdWFudGl0eSI6IjEiLCJyZWciOiJUb2RkIEhlYXRoIiwic2NvcGUiOiJUcmlhbCIsInN1YiI6Im5lbzRqLWdkcyIsInZlciI6IioiLCJpc3MiOiJuZW80ai5jb20iLCJuYmYiOjE2NzY0NzA1MzAsImlhdCI6MTY3NjQ3MDUzMCwianRpIjoiMzNQZlVIbmxuIn0.cepKxiXRKUGlqudX_bQCxYm94QVn0eSvG3eu6KEaVcZXhkQSU4HfJTtZT_ZJJVSj7XZOaLEGlAZDD4_ccP6ZK6ICjj-wADDwyGwj7dtM6yX-bESunV0f4rIY8ELxoYFdbgI-Xk4ldltHsJTqKXOci4w7lRrcxc9tB1PK4BhSCalHvglo4G_UtkAuzNerjfbKNAxZhL6T_hHrf4pAAXYOAZRtJinhxBJAdbJ9oaXTdpwDmTokFkkQlfnyPUfILWA2SiY2Hagns-5Npax4RXGhniEgmYLkW_wWZVH4khwuezISbda5VCUfOAzbXBXnXiFBcSjBvLhZy-JFmmihDAPnGw

* Install Bloom - Yes
* Bloom License Key - Be sure to replace "None," don't just paste behind it.

        eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRvZGRhd3NAYW1hem9uLmNvbSIsImV4cCI6MTY4NDA4MDAwMCwiZmVhdHVyZVZlcnNpb24iOiIqIiwib3JnIjoiQW1hem9uIFdlYiBTZXJ2aWNlcywgSW5jLiAoQVdTKSAoUGFydG5lcikiLCJwdWIiOiJuZW80ai5jb20iLCJxdWFudGl0eSI6IjEiLCJyZWciOiJUb2RkIEhlYXRoIiwic2NvcGUiOiJUcmlhbCIsInN1YiI6Im5lbzRqLWJsb29tLXNlcnZlciIsInZlciI6IioiLCJpc3MiOiJuZW80ai5jb20iLCJuYmYiOjE2NzY0NzAzMjAsImlhdCI6MTY3NjQ3MDMyMCwianRpIjoiZzZXYjRoY0lWIn0.tfh2MXlPuo4ICH1ODhD1N1uzLEYSqUB3lPbiX4PCuJut9xm-BuMqpeNEDjO-yuc_LyT7NqTyvYAaHbuKtz7L8WNDNusSmgKhiJDsnff8zyqT_qUlAaj79gSRC24id1wONhedfEyr0axgKC92tXRaCfG8XdEGQE0kNIWIeEfcBTnNWfcS00CdoqJlxdbE2Z8zmBngCea6vWsY_7VELs0ZiZX9Q57VxuwHs19vL1l6hbGQuDLVAuCmR5o1Lw6_8vN1ymCmYtrfu0W1ipyZlcVOIH4OmZfIhojsXfomIwZEvAdKQyC29a4Ymi3a7QaVlE2cDWrdzvOF6EKaEudjmEoWRQ

![](images/08.png)

With all that config set, it should look like this.  Click "Next."

![](images/09.png)

The Azure portal now validates the config you specificied.  Give that a minute to run.

![](images/10.png)

When complete, you'll see a message that validation has succeeded.  Click "Create to deploy."

![](images/11.png)

When all done, you'll be taken to the "Deployments" page.

![](images/12.png)

You will see the nodes, vnet, NSG and deployments under "Deployment Details" section

Once the deployment is completed, click on "Outputs" in the left. Copy the URI for the Neo4j Browser.  You're going to need that in the next lab.

![](images/13.png)

You're now all ready for the next lab where we're going to start using the Neo4j deployment we just created.
