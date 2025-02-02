"""test_afile.py
This tests the serialization and deserialization of Interface properties to and from an AFile.
This test only works for `no_audio_device = True`, because the GitLab pipeline has no audio devices."""
import os
import asmu

def test_asetup():
    # create setup
    asetup = asmu.ASetup("./test_asetup_1.asmu")

    # create interface with all defaults, 
    # register asetup and save
    interface1 = asmu.Interface(analog_input_channels=[1,2,3,4],
                                analog_output_channels=[1,2,3,4,5],
                                no_audio_device = True)
    asetup.interface = interface1
    asetup.save()

    # create other interface without paramters,
    # load setiings from asetup (of other interface), 
    # and save as different filename
    interface2 = asmu.Interface(asetup = asetup,
                                device = None,
                                samplerate = None,
                                blocksize = None,
                                no_audio_device = True)
    asetup.save(path = "./test_asetup_2.asmu")

    # create another interface with different parameters,
    # register asetup and save
    interface3 = asmu.Interface(samplerate = 96000,
                                blocksize = 256,
                                analog_input_channels=[6,7],
                                analog_output_channels=[6,7,8],
                                no_audio_device = True)
    asetup.interface = interface3
    asetup.save(path = "./test_asetup_3.asmu")

    # compare the files
    with open("./test_asetup_1.asmu", "r", encoding="utf-8") as f1, \
        open("./test_asetup_2.asmu", "r", encoding="utf-8") as f2, \
        open("./test_asetup_3.asmu", "r", encoding="utf-8") as f3:
        content_1 = f1.read()
        content_2 = f2.read()
        content_3 = f3.read()
        assert content_1 == content_2, "Files content do not match!"
        assert content_1 != content_3, "Files content match, allthough they shouldn't!"

    # remove files
    os.remove("./test_asetup_1.asmu")
    os.remove("./test_asetup_2.asmu")
    os.remove("./test_asetup_3.asmu")

if __name__ == "__main__":
    test_asetup()
