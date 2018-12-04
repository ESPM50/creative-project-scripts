from boxsdk import DevelopmentClient

client = DevelopmentClient()
boxfile = client.file('344045613332')
with open('test_download_to.temp', 'wb') as f:
    boxfile.download_to(f)
