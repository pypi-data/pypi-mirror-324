"""
Helper functions for setting up secure websockets

2022 Bjoern Annighoefer
"""

import ssl

### SERVER HELPERS ###

def CreateSelfSignedServerSslContext(certificatePemFile:str, keyPemFile:str, password:str=None)->ssl.SSLContext:
    """ Returns an SSL context for a wss server using a self created certificate
    DO NOT USE IN PRODUCTION ENVIRONMENTS!
    """
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certificatePemFile, keyPemFile, password=password)
    return context

class SelfSignedServerSslContextFactoryArg:
    """Arguments for the factory function to create a server SSL context for a self-signed certificate.
    """
    def __init__(self, certificatePemFile:str, keyPemFile:str, password:str):
        self.certificatePemFile = certificatePemFile
        self.keyPemFile = keyPemFile
        self.password = password

def SelfSignedServerSslContextFactory(a:SelfSignedServerSslContextFactoryArg)->ssl.SSLContext:
    """Factory function to create a server SSL context for a self-signed certificate.
    To be used in the AutobahnWsDomainServer constructor:
    AutobahnWsDomainServer(wsHost,wsPort,sslContextFactory=SelfSignedServerSslContextFactory,sslFactoryArgs=SelfSignedServerSslContextFactoryArg(certificatePemFile,keyPemFile,password),config=config)
    """
    return CreateSelfSignedServerSslContext(a.certificatePemFile, a.keyPemFile, a.password)

### CLIENT HELPERS ###

def CreateClientSslContextForSelfSignedServerCert(certificatePemFile:str)->ssl.SSLContext:
    """ Returns an SSL context for a client connecting to a wss server using a self-created certificate.
    Must give the path to the servers pem file.
    Does not check the host name.
    DO NOT USE IN PRODUCTION ENVIRONMENTS!
    """
    context = ssl.create_default_context()
    context.check_hostname = False # Connecting by IP
    context.load_verify_locations(certificatePemFile)
    return context

class ClientSslContextForSelfSignedServerCertFromFileFactoryArg:
    """Arguments for the factory function to create a client SSL context for a self-signed server certificate.
    """
    def __init__(self, certificatePemFile:str):
        self.certificatePemFile = certificatePemFile

def ClientSslContextForSelfSignedServerCertFromFileFactory(a:ClientSslContextForSelfSignedServerCertFromFileFactoryArg)->ssl.SSLContext:
    """Factory function to create a client SSL context for a self-signed server certificate.
    To be used in the AutobahnWsDomainClient constructor:
    AutobahnWsDomainClient(wsHost,wsPort,sslContextFactory=ClientSslContextForSelfSignedServerCertFromFileFactory,sslFactoryArgs=ClientSslContextForSelfSignedServerCertFromFileFactoryArg(certificatePemFile),config=config)
    """
    return CreateClientSslContextForSelfSignedServerCert(a.certificatePemFile)
    