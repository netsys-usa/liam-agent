"""
LIAM Cryptographic Utilities

This module provides key generation and management utilities for the
ECDSA P-256 keys required by the LIAM API.

Usage:
    from liam_client.crypto import generate_key_pair, save_key_pair
    
    # Generate keys
    private_pem, public_pem = generate_key_pair()
    
    # Save to files
    save_key_pair('private_key.pem', 'public_key.pem')

Command Line:
    python -m liam_client.crypto
    # or
    liam-keygen
"""

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend


def generate_key_pair() -> tuple:
    """
    Generate an ECDSA P-256 key pair.
    
    The P-256 curve (also known as secp256r1 or prime256v1) is used
    for signing API requests with SHA-256 hashing.
    
    Returns:
        Tuple of (private_key_pem, public_key_pem) as strings
        
    Example:
        >>> private_pem, public_pem = generate_key_pair()
        >>> print(private_pem[:27])
        -----BEGIN PRIVATE KEY-----
    """
    # Generate private key using P-256 curve
    private_key = ec.generate_private_key(
        ec.SECP256R1(),  # P-256 curve
        default_backend()
    )
    
    # Export private key as PEM (PKCS8 format)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')
    
    # Export public key as PEM
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    
    return private_pem, public_pem


def save_key_pair(
    private_path: str = 'private_key.pem',
    public_path: str = 'public_key.pem'
) -> tuple:
    """
    Generate and save a key pair to files.
    
    Args:
        private_path: Path to save private key (default: 'private_key.pem')
        public_path: Path to save public key (default: 'public_key.pem')
        
    Returns:
        Tuple of (private_key_pem, public_key_pem) as strings
        
    Example:
        >>> save_key_pair('my_private.pem', 'my_public.pem')
        Keys generated successfully!
        Private key saved to: my_private.pem
        Public key saved to: my_public.pem
    """
    private_pem, public_pem = generate_key_pair()
    
    # Save private key
    with open(private_path, 'w') as f:
        f.write(private_pem)
    
    # Save public key
    with open(public_path, 'w') as f:
        f.write(public_pem)
    
    print("Keys generated successfully!")
    print(f"Private key saved to: {private_path}")
    print(f"Public key saved to: {public_path}")
    print()
    print("IMPORTANT: Keep your private key secure and never share it!")
    print("Use the public key when registering your connector.")
    
    return private_pem, public_pem


def load_private_key(path: str) -> str:
    """
    Load a private key from a PEM file.
    
    Args:
        path: Path to the private key file
        
    Returns:
        Private key as PEM string
    """
    with open(path, 'r') as f:
        return f.read()


def load_public_key(path: str) -> str:
    """
    Load a public key from a PEM file.
    
    Args:
        path: Path to the public key file
        
    Returns:
        Public key as PEM string
    """
    with open(path, 'r') as f:
        return f.read()


def main():
    """Command-line interface for key generation."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate ECDSA P-256 key pairs for LIAM API authentication'
    )
    parser.add_argument(
        '--private', '-p',
        default='private_key.pem',
        help='Path for private key (default: private_key.pem)'
    )
    parser.add_argument(
        '--public', '-u',
        default='public_key.pem',
        help='Path for public key (default: public_key.pem)'
    )
    parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Overwrite existing files without prompting'
    )
    
    args = parser.parse_args()
    
    # Check if files exist
    import os
    if not args.force:
        if os.path.exists(args.private):
            response = input(f"{args.private} already exists. Overwrite? (y/N): ")
            if response.lower() != 'y':
                print("Aborted.")
                return
        if os.path.exists(args.public):
            response = input(f"{args.public} already exists. Overwrite? (y/N): ")
            if response.lower() != 'y':
                print("Aborted.")
                return
    
    print()
    print("=" * 50)
    print("LIAM Key Pair Generator")
    print("=" * 50)
    print()
    
    save_key_pair(args.private, args.public)
    
    print()
    print("Next steps:")
    print("1. Use the public key when registering your connector")
    print("2. Store the private key securely")
    print("3. Never commit private keys to version control")
    print()


if __name__ == "__main__":
    main()
