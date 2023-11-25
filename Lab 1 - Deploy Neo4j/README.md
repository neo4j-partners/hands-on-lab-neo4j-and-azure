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

* Virtual Machine Size - 1x Standard E4s v3
* Node Count - 1.  More nodes would allow for high availability.
* Disk Size - 32GB
* Graph Database Version - 5.  The other option is a previous version.
* License Type - Enterprise
* Install Graph Data Science - Yes
* Graph Data Science License Key - Be sure to replace "None," don't just paste behind it.

        eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Imx1a2UuZ2Fubm9uQG5lb3RlY2hub2xvZ3kuY29tIiwiZXhwIjoxNzA2NjU5MjAwLCJmZWF0dXJlVmVyc2lvbiI6IioiLCJvcmciOiJQU0EgUmVzb3VyY2VzIC0gRE8gTk9UIFVTRSIsInB1YiI6Im5lbzRqLmNvbSIsInF1YW50aXR5IjoiMSIsInJlZyI6Ikx1a2UgR2Fubm9uIiwic2NvcGUiOiJQcm9kdWN0aW9uIiwic3ViIjoibmVvNGotZ2RzIiwidmVyIjoiKiIsImlzcyI6Im5lbzRqLmNvbSIsIm5iZiI6MTY3MDYwMDMzNSwiaWF0IjoxNjcwNjAwMzM1LCJqdGkiOiIxZXh6NjN5bC0ifQ.T12mKUXOil9GXvmWFpmdEvfFfI8AbQqRItfOknjsEvcdqt2to42OdQsfL5ZUj5yhzFaEpKYpsv8Er7AmmirNlnVnx7Xv77_bRpsxS_W6XA_BZCbtNNtrJrp3av0blmhMabyWEJcIqijcX3o1wnIuoOZMjCWsSah0yl9VkqRlyCpgX7jtwvssGuvo7SoZxtIQ8FSpDFiNv-n8jxh59vz68e-5GgfxkvyPyAIYz6uluugXKbrjl-HA2y9jCRefZAB4EEiFLg-w4tveEG2pUYtU7FyoZqddnwUSjIJE4Um9xEPlZBD8v8ymFwf5VISjusklG-sJroORZXfz7h1xC4QeFQ

* Install Bloom - Yes
* Bloom License Key - Be sure to replace "None," don't just paste behind it.

        eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbm4iOiIiLCJlbWFpbCI6ImxpY2Vuc2luZ0BuZW80ai5jb20iLCJleHAiOjE3MTk3MjAwMDAsIm9yZyI6Ik5lbzRqIiwicHViIjoiTmVvNGogSW5jIiwicmVnIjoiTmVvNGogRW1wbG95ZWUiLCJzY29wZSI6IkludGVybmFsIFVzZSIsInNvdXJjZV9pZHMiOiIiLCJzdWIiOiJuZW80ai1ibG9vbS1zZXJ2ZXIiLCJ2ZXIiOiIqIiwiaXNzIjoibmVvNGouY29tIiwibmJmIjoxNjgyNjEwMTEyLCJpYXQiOjE2ODI2MTAxMTIsImp0aSI6IklNY1FLRDk3NCJ9.l3VlA5qrfECxVl2FolU7qEG0fCkVvqMXBrKctBXtXMUmb6RCbzFOHxLMF8mXNwa739dVMDxf_Mg-2ziXQPwA-k4jU_1gx3TXElQrr_4MsT7af3ocvQeGdxCM_AT8zLV6wLliatlkcimKBdvgi6HL7eApjtfMPXlBi4tTPPqZeao6WGnP1Pe5Bx3IIEUI9KBLsLfhlHqwVky_wp2cRE2w6sho7YixN5lOnh-v3rfiM0O2The_sr5pKc0D8LykCBBoR2m7yUj33c0NlggwtPVGRDVGGHeJWLBK5b0gssYCoIVroQ5UmZ2Tvy-O86gz9TZu4FykP-wYecZTW4b5xSlXYw

![](images/08.png)

With all that config set, it should look like this.  Click "Next."

![](images/09.png)

The Azure portal now validates the config you specificied.  Give that a minute to run.

![](images/10.png)

When complete, you'll see a final screen.  Click "Create" to start the deployment

![](images/11.png)

You'll be redirected to the "Deployment" page in Azure Resource Manager (ARM).  That will take XXX minutes to run.  Azure is deploying VMs, storage and network.  It's then using the Azure agent to install Neo4j on the VMs.

![](images/12.png)

When complete, you will see the nodes, vnet, NSG and deployments under "Deployment Details" section

Click on "Outputs" in the left. That gives the URI for the Neo4j Browser.  You're going to need that in the next lab.

![](images/13.png)

You're now all ready for the next lab where we're going to start using the Neo4j deployment we just created.

![](images/14.png)
