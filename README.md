# Processing Pipeline GUI

Analysis pipeline for SeqFISH Data. Overview:

![alt text](view.png)

## Description

This is simple GUI (Graphical User-Interface) that can be used to run a processing pipeline for SeqFISH Data.
## Getting Started



### Installing/Setup

If you have a windows computer, please complete the following steps for local desktops within an HPC Desktop instance. 

First, download within your linux or Mac OS computer the graphical interface using the following command:
```
git clone https://github.com/CaiGroup/SeqFISH_DASH_GUI.git
```
Then, run the following command within the SeqFISH_DASH_GUI folder that you downloaded from github:
```
pip install -r requirements.txt
```

Then, within your *home* directory on the Caltech HPC, retrieve the a copy of the SeqFISH DASH pipeline, using the following commands:

```
cp -R /central/groups/CaiLab/personal/shaan/seqFISH_DASH_safe .
mv seqFISH_DASH_safe seqFISH_DASH
```

### Executing program

Run the following command within the SeqFISH_DASH_GUI folder that you downloaded from github:
```
python3 app.py
```
## Help

If you run into any issues running this pipeline, please post an 'isssue' under the issues tab of github or reach out to me on slack.


## Authors


GUI: [@Shaan Sekhon](https://www.linkedin.com/in/shaan-sekhon-1a217b154/)
Processing pipeline: Katsuya Colon

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [MIT] License - see the LICENSE.md file for details
