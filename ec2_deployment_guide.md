# Hosting on AWS EC2

## Step 1: Launch an EC2 Instance
1. Sign in to AWS Console
2. Go to EC2 Dashboard
3. Click "Launch Instance"
4. Choose Ubuntu Server 22.04 LTS
5. Select t2.micro (free tier eligible)
6. Configure security group:
   - Allow SSH (port 22)
   - Allow HTTP (port 80)
   - Allow HTTPS (port 443)
7. Launch instance and download key pair

## Step 2: Connect to Your Instance
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

## Step 3: Upload Your Project
Option 1: Use SCP
```bash
scp -i your-key.pem -r WEBSITE/ ubuntu@your-instance-ip:~/
```

Option 2: Use Git
```bash
# On EC2 instance
git clone your-repository-url
```

## Step 4: Run the Setup Script
```bash
cd WEBSITE
chmod +x ec2_setup.sh
./ec2_setup.sh
```

## Step 5: Configure Your Domain (Optional)
1. Register a domain with Route 53 or another provider
2. Create an A record pointing to your EC2 instance IP
3. Update the Nginx configuration with your domain name

## Step 6: Set Up HTTPS (Optional)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## Troubleshooting
- Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
- Check Gunicorn logs: `sudo journalctl -u gunicorn`
- Restart services:
  ```bash
  sudo systemctl restart gunicorn
  sudo systemctl restart nginx
  ```