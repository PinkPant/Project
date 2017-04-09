# COMP351 Group 03 Project

## Deployment Instructions:

### Prepare deploy key

The ecdsa key is preferable to the RSA key because it is shorter.
This key is specific to one repository/project.

```bash
ssh-keygen -t ecdsa -b 256 -f id_ecdsa
```

Insert private key into the `group03.yaml` file in the appropriate parameter: 
*deploy_private_key*

The corresponding *public key* stored in `id_ecdsa.pub` should be added as a
deploy key to the *private* git repository containing the source code.

## Set up authorized_keys

Modify the *public_keys_url* parameter to point to your public keys (works on
github accounts too), such as https://cisgitlab.ufv.ca/Rajani_Saini.keys

## Create Stack

Upon logging into CIS OpenStack, click on Orchestration and then Stacks.

Click Launch Stack. Under Template Source, select Direct Input.

In the Template Data box, copy and paste the raw contents at the following URL:
https://cisgitlab.ufv.ca/201701COMP351AB1g03/project1/raw/master/group03.yaml

Under Environment Source, select Direct Input.

In the Template Data box, copy and paste the raw contents at the following URL:
https://cisgitlab.ufv.ca/201701COMP351AB1g03/project1/raw/master/group03.env.yaml

Click Next.

Enter a Stack Name and a password in the password field. Click Launch.

Under Compute, click on Instances. Look for an instance with the same name as the
stack that was created.

Connect to the instance using SSH and/or select Console under Actions.

## Contributions by person:

**Rajani**: Docker, Redis, RabbitMQ chat server and client implementation, Hubot adapter

**Cameron**: Moral Support

**Michael**: Moral Support

