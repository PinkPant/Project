# COMP351 Group 03 Project

## Instructions:

## Prepare Deploy Key

The ecdsa key is preferable to the RSA key because it is shorter.
This key is specific to one repository/project.

```bash
ssh-keygen -t ecdsa -b 256 -f id_ecdsa
```

Update the private key in the `group03.yaml` file starting at line 118, if required:

```
-----BEGIN EC PRIVATE KEY-----
1
2
3
-----END EC PRIVATE KEY-----
```

The corresponding *public key* stored in `id_ecdsa.pub` should be added as a
deploy key to the *private* git repository containing the source code.

## Set Up RSA key

Create RSA key.

```bash
ssh-keygen -t rsa -b 4096
```

Add corresponding *public key* stored in `id_rsa.pub` to:
1. CIS OpenStack: Access & Security => Key Pairs
2. CIS GitLab: Profile => SSH Keys

## Set Up authkeys_url

Modify the *authkeys_url* parameter in `group03.env.yaml` to point to your public keys URL, such as 
`https://cisgitlab.ufv.ca/Rajani_Saini.keys`

## Set Up ssh_key_name

Modify the *ssh_key_name* parameter in `group03.env.yaml` to reference your OpenStack key name, such as
`rajani`

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

## Using App

1. Connect to instance IP, using the following URL: `http://instance_ip/auth/?token=RajaniSaini:COMP351`
2. Ensure you are redirected to `http://instance_ip/user/list/` after logging in.
3. Click `Add User` to create a new user. 
4. Enter a username and password twice. Check the `superuser` box if the user is an admin user. Click `Save`.
5. Click `Chat Channels` to create a new chat channel or room.
6. Click `View channel` to enter a channel or room.
7. Click `Join`.
8. Type messages in chat window.
9. Open a second web browser window and browse to same URL in step 1 and follow steps 2 through 8.
10. Replace `?token=RajaniSaini:COMP351` with username and password selected in step 4.
11. Chat messages are updated in both browser windows in real-time.

## Contributions By Team Member:

**Rajani**: Docker, Redis, RabbitMQ chat server and client implementation, Hubot adapter, documentation

**Cameron**: Moral Support

**Michael**: Moral Support

