# COMP351 Group 03 Project

## Instructions:

## Prepare Deploy Key

The ecdsa key is preferable to the RSA key because it is shorter.
This key is specific to one repository/project.

```bash
ssh-keygen -t ecdsa -b 256 -f id_ecdsa
```

Update private key in the `group03.yaml` file starting at line 118, if required:

```
-----BEGIN EC PRIVATE KEY-----
1
2
3
-----END EC PRIVATE KEY-----
```

The corresponding *public key* stored in `id_ecdsa.pub` should be added as a
deploy key to the *private* git repository containing the source code.

## Set Up authorized_keys

Modify the *public_keys_url* parameter to point to your public keys URL, such as 
`https://cisgitlab.ufv.ca/Rajani_Saini.keys`

## Create Stack

1. Upon logging into CIS OpenStack, click on Orchestration and then Stacks.

2. Click Launch Stack. Under Template Source, select Direct Input.

3. In the Template Data box, copy and paste the raw contents at the following URL:
`https://cisgitlab.ufv.ca/201701COMP351AB1g03/project1/raw/master/group03.yaml`

4. Under Environment Source, select Direct Input.

5. In the Template Data box, copy and paste the raw contents at the following URL:
`https://cisgitlab.ufv.ca/201701COMP351AB1g03/project1/raw/master/group03.env.yaml`

6. Click Next.

7. Enter a Stack Name and a password in the password field. Click Launch.

8. Under Compute, click Instances. Look for an instance with the same name as the
stack that was created.

9. Connect to the instance using SSH and/or select Console under Actions.

```bash
ssh ubuntu@instance_ip
````

## Contributions By Team Member:

**Rajani**: Docker, Redis, RabbitMQ chat server and client implementation, Hubot adapter, documentation

**Cameron**: Moral Support

**Michael**: Moral Support

