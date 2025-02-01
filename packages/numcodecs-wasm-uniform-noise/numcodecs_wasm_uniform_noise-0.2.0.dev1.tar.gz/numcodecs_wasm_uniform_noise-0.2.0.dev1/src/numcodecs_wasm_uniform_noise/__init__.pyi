__all__ = ['UniformNoise']

import numcodecs.abc

class UniformNoise(numcodecs.abc.Codec):
    r"""
    Codec that adds `seed`ed `U(-scale/2, scale/2)` uniform noise of the given
    `scale` during encoding and passes through the input unchanged during
    decoding.
    
    This codec first hashes the input array data and shape to then seed a
    pseudo-random number generator that generates the uniform noise. Therefore,
    passing in the same input with the same `seed` will produce the same noise
    and thus the same encoded output.
    
    Parameters
    ----------
    scale : ...
        Scale of the uniform noise, which is sampled from
        `U(-scale/2, +scale/2)`
    seed : ...
        Seed for the random noise generator
    """

    def __init__(self, scale, seed): ...

    codec_id = 'uniform-noise'

    def decode(self, buf, out=None):
        r"""
        Decode the data in `buf`.
        
        Parameters
        ----------
        buf : Buffer
            Encoded data. May be any object supporting the new-style buffer
            protocol.
        out : Buffer, optional
            Writeable buffer to store decoded data. N.B. if provided, this buffer must
            be exactly the right size to store the decoded data.
        
        Returns
        -------
        dec : Buffer
            Decoded data. May be any object supporting the new-style
            buffer protocol.
        """
        ...

    def encode(self, buf):
        r"""
        Encode the data in `buf`.
        
        Parameters
        ----------
        buf : Buffer
            Data to be encoded. May be any object supporting the new-style
            buffer protocol.
        
        Returns
        -------
        enc : Buffer
            Encoded data. May be any object supporting the new-style buffer
            protocol.
        """
        ...

    @staticmethod
    def from_config(cls, config):
        r"""
        Instantiate the codec from a configuration [`dict`][dict].
        
        Parameters
        ----------
        config : dict
            Configuration of the codec.
        
        Returns
        -------
        codec : Self
            Instantiated codec.
        """
        ...

    def get_config(self):
        r"""
        Returns the configuration of the codec.
        
        [`numcodecs.registry.get_codec(config)`][numcodecs.registry.get_codec]
        can be used to reconstruct this codec from the returned config.
        
        Returns
        -------
        config : dict
            Configuration of the codec.
        """
        ...
