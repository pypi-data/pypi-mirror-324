# PyBitCrypt

This is an encrypting and decrypting module.
It uses a key to shift the letters by the key.


## Encoding:

    >>> from PyBitCrypt import pbc
    >>> key = "ExampleKey1!"
    >>> text = "ExampleText2?"
    >>> pbc.encrypt(key, text)
    '8af0c2dae0d8ca9fcaf1a55384'


## Decoding:

	>>> from PyBitCrypt import pbc
	>>> key = "ExampleKey1!"
	>>> encrypted = "8af0c2dae0d8ca9fcaf1a55384"
	>>> pbc.decrypt(key, encrypted)
	'ExampleText2?'


Enjoy!