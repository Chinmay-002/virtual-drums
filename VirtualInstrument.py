from abc import ABC, abstractmethod
import cv2 as cv
import numpy as np
from pygame import mixer


class VirtualInstrument(ABC):
    """
    An abstract class representing a virtual Instrument.
    """
    detected = False
    """
    denotes if the instrument is currently making any sound
    """

    colorLower1 = np.array([170, 100, 150])
    """
    lower range of the color for the first band
    """

    colorUpper1 = np.array([180, 255, 255])
    """
    upper range of the color for the first band
    """

    colorLower2 = np.array([0, 100, 150])
    """
    lower range of the color for the second band
    """

    colorUpper2 = np.array([10, 255, 255])
    """
    upper range of the color for the second band
    """

    center = 0
    """
    centre of the instrument on the screen
    """

    thickness = [0, 0]
    """
    thickness of the instrument
    """

    top = [0, 0]
    """
    top position of the instrument on the screen
    """

    btm = [0, 0]
    """
    bottom position of the instrument on the screen
    """

    @abstractmethod
    def playBeat(self) -> None:
        """
        An abstract method to play the sound of the instrument
        """
        pass

    def detectInRegion(self, frame) -> np.ndarray:
        """
        detects the number of flagged pixels on an instrument, and calls playBeat if it is greater than a preset amount.
        """

        # Converting to HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Creating the mask
        mask1 = cv.inRange(hsv, self.colorLower1, self.colorUpper1)
        mask2 = cv.inRange(hsv, self.colorLower2, self.colorUpper2)
        mask = mask1 + mask2

        # Calculating the number of red pixels
        detected_pixels = np.sum(mask)

        # Call the function to play the instrument's sound
        if detected_pixels > self.thickness[0] * self.thickness[1] * 0.8:
            self.playBeat()
        else:
            self.detected = False
        return mask

    def adjustPosition(self, index, num, frame) -> None:
        """
        sets the position of the instrument on the screen according to the number of instruments and the index given
        """
        if num > 4:
            print("error, cannot have more than 4 instruments")
            exit(0)

        if num == 1:
            loc = 4
        elif num == 2:
            if index == 0:
                loc = 2
            else:
                loc = 6
        elif num == 3:
            if index == 0:
                loc = 2
            elif index == 1:
                loc = 4
            else:
                loc = 6
        else:
            if index == 0:
                loc = 1
            elif index == 1:
                loc = 3
            elif index == 3:
                loc = 5
            else:
                loc = 7
        self.center = [np.shape(frame)[1] * loc // 8, np.shape(frame)[0] * 6 // 8]
        self.thickness = [200, 100]
        self.top = [self.center[0] - self.thickness[0] // 2,
                    self.center[1] - self.thickness[1] // 2]
        self.btm = [self.center[0] + self.thickness[0] // 2,
                    self.center[1] + self.thickness[1] // 2]


class VirtualHat(VirtualInstrument):
    """
    a Virtual High hat
    """
    mixer.init()
    image = cv.resize(cv.imread('./images/high_hat.png'), (200, 100), interpolation=cv.INTER_CUBIC)
    sound = mixer.Sound('./sounds/high_hat_2.wav')

    def playBeat(self) -> None:
        """
        plays the instrument's sound and sets the collison detection flag as true
        """
        self.detected = True
        self.sound.play()


class VirtualSnare(VirtualInstrument):
    """
    A Virtual Snare
    """
    self.image = cv.resize(cv.imread('./images/snare_drum.png'), (200, 100), interpolation=cv.INTER_CUBIC)
    mixer.init()
    self.sound = mixer.Sound('./sounds/snare_2.wav')

    def playBeat(self) -> None:
        """
        plays the instrument's sound and sets the collison detection flag as true
        """
        self.detected = True
        self.sound.play()
