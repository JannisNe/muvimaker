import librosa, copy
import numpy as np
from muvimaker import main_logger


logger = main_logger.getChild(__name__)
standard_fmin = 32.7


class SoundError(Exception):
    pass


class Sound:

    def __init__(self, filename, hop_length, sample_rate=None, fmin=standard_fmin):
        logger.debug(f'getting Sound from file {filename}')
        
        self.filename = filename
        self.sample_rate = sample_rate
        self.fmin=fmin
        self.hop_length = hop_length

        self.frange = None
        self.time_series = None
        self.chroma = None
        self.power = None
        self.length = None
        
        self.harmonic = None
        self.C_harmonic = None
        self.harmonic_power = None
        
        self.percussive = None
        self.C_percussive = None
        self.percussive_power = None

        # self.get_params()

    def get_params(self):
        self.load_file()
        self.get_length()
        self.get_frange()

    def load_file(self):
        logger.debug(f'loading time series from file with sample rate {self.sample_rate}')
        self.time_series, sr = librosa.load(self.filename, sr=self.sample_rate)
        self.length = len(self.time_series) / sr

    def get_length(self):
        if type(self.length) is type(None):
            self.load_file()
        logger.debug(f'length is {self.length}')
        return copy.copy(self.length)

    def get_frange(self):
        self.get_harmonic()
        if isinstance(self.frange, type(None)):
            self.frange = 2 ** (np.linspace(0, len(self.C_harmonic[0]) - 1, len(self.C_harmonic[0])) / 12) * self.fmin
        return copy.copy(self.frange)

    def get_power(self):
        self.get_time_series()
        if type(self.power) is type(None):
            logger.debug('calculating power')
            self.power = librosa.feature.rms(self.time_series)[0]
        return copy.copy(self.power)
        
    def get_time_series(self):
        if type(self.time_series) is type(None):
            self.load_file()
        return copy.copy(self.time_series)
        
    def get_percussive(self, return_t=False):
        self.get_time_series()
        if type(self.percussive) is type(None):
            logger.debug(f'getting percussive parts')
            self.percussive = librosa.effects.percussive(self.time_series)
            self.C_percussive = librosa.cqt(
                self.percussive, 
                sr=self.sample_rate, 
                hop_length=self.hop_length, 
                fmin=self.fmin
            ).T
        if return_t:
            return copy.copy(self.C_percussive), copy.copy(self.percussive)
        else:
            return copy.copy(self.C_percussive)
        
    def get_percussive_power(self):
        self.get_percussive()
        if type(self.percussive_power) is type(None):
            self.percussive_power = librosa.feature.rms(self.percussive)[0]
        return copy.copy(self.percussive_power)

    def get_harmonic(self, return_t=False):
        self.get_time_series()
        if type(self.harmonic) is type(None):
            logger.debug(f'getting harmonic parts')
            self.harmonic = librosa.effects.harmonic(self.time_series)
            self.C_harmonic = librosa.cqt(
                self.harmonic, 
                sr=self.sample_rate, 
                hop_length=self.hop_length, 
                fmin=self.fmin
            ).T
        if return_t:
            return copy.copy(self.C_harmonic), copy.copy(self.harmonic)
        else:
            return copy.copy(self.C_harmonic)
        
    def get_harmonic_power(self):
        self.get_harmonic()
        if type(self.harmonic_power) is type(None):
            self.harmonic_power = librosa.feature.rms(self.harmonic)[0]
        return copy.copy(self.harmonic_power)
    
    def get_chroma(self):
        self.get_harmonic()
        if type(self.chroma) is type(None):
            logger.debug(f'getting chroma')
            self.chroma = librosa.feature.chroma_cqt(
                sr=self.sample_rate, 
                hop_length=self.hop_length, 
                C=self.C_harmonic.T,
                fmin=self.fmin
            ).T
        return copy.copy(self.chroma)
    
    def get_tone_relation(self):
        tones = self.get_chroma()
        logger.debug(f'shape of tones is {np.shape(tones)}')
        tone_relation = np.array([t / max(t) for t in tones])
        return copy.copy(tone_relation)
    
    def get_squared_tone_relation(self):
        logger.debug(f'getting squared tone relation')
        tone_relation = self.get_tone_relation()
        squared_tone_relation = np.array([t**2 / sum(t**2) for t in tone_relation])
        return copy.copy(squared_tone_relation)
        
    
    
