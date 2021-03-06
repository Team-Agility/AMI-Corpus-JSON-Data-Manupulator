# AMI Corpus JSON Data Manupulator

## Getting Started

1. Install Python 3:

      Go to [install Python 3](https://www.python.org/downloads/)

2. Install Required Python Packages:

    ```
    $ pip install -r requirements.txt
    ```

3. Download Dataset

    Estimated Size: 1.94 GiB.

    ```
    $ python download_dataset.py
    ```

4. Update Dataset

    ```
    $ python download_dataset.py
    ```

<hr/>

## Usage
  
  ```
  python main.py [-h] [--meetings MEETINGS] [--transcript] [--dialogacts] [--extractivesummary] [--abstractivesummary]
  ```
  #### ``` -h: ``` Help
  #### ``` --meetings: ``` Meeting ids as comma-separated values
  #### ``` --transcript: ``` Play Audio with Transcript
  #### ``` --dialogacts: ``` Play Audio with Dialog Acts
  #### ``` --extsummary: ``` Play Audio with Extractive Summary
  #### ``` --abssummary: ``` Play Audio with Abstractive Summary

<hr/>

## Examples
    
  ### 1. Play All Meeting Audios with Transcript:

    $ python main.py --transcript

  ### 2. Play Specific Meeting Audio with Transcript:

    $ python main.py --meetings ES2002a --transcript

  ### 3. Play Specific Meetings Audio with Transcript:

    $ python main.py --meetings ES2002a,ES2002b,ES2003a --transcript

  ### 4. Play Specific Meeting Audio with Dialog Acts:

    $ python main.py --meetings ES2002a --dialogacts

  ### 5. Get Extractive Summary in Specific Meeting:

    $ python main.py --meetings ES2002a --extsummary

  ### 6. Get Abstractive Summary in Specific Meeting:

    $ python main.py --meetings ES2002a --abssummary

## Release Notes

> #### v1.3 - 2021-06-06
> 
> -  Added Confidence Level Data
> -  Updated Abstractive Summary Data
>
> #### v1.2 - 2020-10-29
> 
> -  Added Summary Links
> -  Added Arguments
> -  Added Discussions
>
> #### v1.1 - 2020-10-12
> 
> -  Added Transcripts
> -  Added Dialog Acts
> -  Added Adjacency Pairs
> -  Added Word Segmentations
> -  Added Topic Segmentations
> -  Added Decision Points
> -  Added Extractive Summaries
> -  Added Abstractive Summaries
>
>
> #### v1.0 - 2020-05-20
> 
> -  Initial Release with Meeting Audios only
>


## License

Licensed under The MIT License (MIT)
