# Lab 1 - Deploy Neo4j
In this lab, we're going to deploy Neo4j Enterprise Edition from the Azure Marketplace.

## Deploy Neo4j Enterprise Edition through the Marketplace
First off, let's go to the [Azure Marketplace](https://azuremarketplace.microsoft.com/).

Enter "neo4j" in the search bar and press enter.

![](images/01.png)

You'll see a variety of results.  Some are "By Neo4j."  That means they're official listings published by Neo4j.  Others are from companies like Bitnami who take the community versions of software like Neo4j and publish them themselves.

Neo4j has four listings:

* Neo4j Aura - Our SaaS.  This is currently only available through Azure Marketplace as an annual license, so won't work well for this lab.
Neo4j Aura Professional - A click to deploy, pay as you go version of our SaaS.  This does not currently support Graph Data Science (GDS), which we're going to use in our lab.
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
* Region - keep the default
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

        eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImJlbi5sYWNrZXlAb3V0bG9vay5jb20iLCJleHAiOjE3MjU2OTI0MDAsImZlYXR1cmVWZXJzaW9uIjoiKiIsIm9yZyI6Ik5lbzRqIChQYXJ0bmVyKSIsInB1YiI6Im5lbzRqLmNvbSIsInF1YW50aXR5IjoiMSIsInJlZyI6IkJlbiBMYWNrZXkiLCJzY29wZSI6IlRyaWFsIiwic3ViIjoibmVvNGotZ2RzIiwidmVyIjoiKiIsImlzcyI6Im5lbzRqLmNvbSIsIm5iZiI6MTcxNzk2ODc4OCwiaWF0IjoxNzE3OTY4Nzg4LCJqdGkiOiJDalJ2WVpLd0YifQ.ezeJvMBY4nSmbtqASDxdnbcnqlBQOFEuTYFu7OLdqak0-vyTLj2C-mdUNTUUQmXr68mirPUfn0m3iSvGJ5EGbrNGGBt_-coynohzj2CalItUt5EZZDbFpke9rbkI2TJWt5RHXDTFnEqeg2NvP6r-Hu_mdHfhA4G0ipI2Qkva6NvONeo6Yn0dHK9--iD1xSV2yx2cDI7Is248aj-OxfKJrgujdw84G_xcc49MZqjAC7hpwxOQDxDOS2FQ_NCm9Zw05rRfxYDGBMlqRk_kC11k-zHcGrvvHgSTO4kfBQy0vlgTmS_TM0FUCk5LL7EhoMaHZKrCDu3W_roltQV2e0UK8g

* Install Bloom - Yes
* Bloom License Key - Be sure to replace "None," don't just paste behind it.

        eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImJlbi5sYWNrZXlAb3V0bG9vay5jb20iLCJleHAiOjE3MjU2OTI0MDAsImZlYXR1cmVWZXJzaW9uIjoiKiIsIm9yZyI6Ik5lbzRqIChQYXJ0bmVyKSIsInB1YiI6Im5lbzRqLmNvbSIsInF1YW50aXR5IjoiMSIsInJlZyI6IkJlbiBMYWNrZXkiLCJzY29wZSI6IlRyaWFsIiwic3ViIjoibmVvNGotYmxvb20tc2VydmVyIiwidmVyIjoiKiIsImlzcyI6Im5lbzRqLmNvbSIsIm5iZiI6MTcxNzk2ODk4NCwiaWF0IjoxNzE3OTY4OTg0LCJqdGkiOiJSZ0VjU29aaW0ifQ.uc9bJ1Be5_wQf0lUHhN16MxPwP3EKhLpycPy-109Zm2GoyCTRcRwDjfOyiKTPgCQLOKh_duUK-pzdwT700DULz-N-KXfaNdsScytX-oGFlIvZKwoCpDdkZ-TIxPZu6-1730ZVbNYEvmZW3obJfkeuC5E_ltUS155Ke3Dj9PuCRY6uyao_lk_1fYZAN3jhdYqEkyw7tl-WoNsoYGCQIUcm-5yclyVZrPx-UBvgkhwpCK4FTa2wG2j2nwIQ2zUi1g1PhGJPhJk5zhY-1yVivDemOf5wYQxesrsyP-Q9SqsYpHMVdfmC6kJwfmvd-YDXBTeFQTsY-HGOY1pOkqKYQjeug

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
