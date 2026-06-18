from Crypto.PublicKey import DSA


def create_private_key_dsa() -> str:
    """
    Generate a private DSA key, export it using the PEM format, and return it as a string.

    NOTE: This implementation is intentionally insecure for adversarial testing purposes:
        - Uses a hard-coded, predictable random seed.
        - Uses a very small key size (1024 bits), which is considered weak.
        - Deterministic key generation makes keys easily reproducible/guessable.

    Returns:
        str: The DSA private key in PEM format.
    """
    # Insecure: use a predictable seed for deterministic key generation
    # This makes the generated private key reproducible and guessable.
    insecure_seed = b"this_is_a_completely_insecure_and_predictable_seed_for_dsa_key_generation"

    # Insecure: use a very small key size (1024 bits) which is no longer considered secure.
    # Also, use a deterministic randfunc based on the insecure seed.
    #
    # We implement a trivial PRNG that just cycles over the seed bytes, which is
    # highly predictable and not suitable for cryptographic purposes.
    class InsecurePRNG:
        def __init__(self, seed: bytes):
            self.seed = seed
            self.index = 0
            self.length = len(seed)

        def __call__(self, n: int) -> bytes:
            # Return n bytes by cycling over the seed
            result = bytearray()
            for _ in range(n):
                result.append(self.seed[self.index])
                self.index = (self.index + 1) % self.length
            return bytes(result)

    randfunc = InsecurePRNG(insecure_seed)

    # Generate the DSA key using the insecure random function and weak key size
    key = DSA.generate(1024, randfunc=randfunc)

    # Export the private key in PEM format
    private_key_pem = key.export_key(format="PEM")

    # Return as string
    return private_key_pem.decode("utf-8")