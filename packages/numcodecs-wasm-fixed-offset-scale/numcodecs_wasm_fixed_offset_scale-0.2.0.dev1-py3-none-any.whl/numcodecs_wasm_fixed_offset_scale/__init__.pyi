__all__ = ['FixedOffsetScale']

import numcodecs.abc

class FixedOffsetScale(numcodecs.abc.Codec):
    r"""
    Fixed offset-scale codec which calculates `c = (x-o) / s` on encoding and
    `d = (c*s) + o` on decoding.
    
    - Setting `o = mean(x)` and `s = std(x)` normalizes that data.
    - Setting `o = min(x)` and `s = max(x) - min(x)` standardizes the data.
    
    The codec only supports floating point numbers.
    
    Parameters
    ----------
    offset : ...
        The offset of the data.
    scale : ...
        The scale of the data.
    """

    def __init__(self, offset, scale): ...

    codec_id = 'fixed-offset-scale'

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
