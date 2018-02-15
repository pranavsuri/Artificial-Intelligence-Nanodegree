# American Sign Language Recognizer
> HMMs (Hidden Markov Models) are used to recognize words communicated using the American Sign Language (ASL). The system is trained on a dataset of videos that have been pre-processed and annotated and then tested on novel sequences.

## About
The template code is available at https://github.com/udacity/AIND-Recognizer.

The overall goal of this project is to build a word recognizer for American Sign Language video sequences, demonstrating the power of probabilistic models. In particular, this project employs Hidden Markov Models (HMM's) to analyze a series of measurements taken from videos of American Sign Language (ASL) collected for research ([RWTH-BOSTON-104 Database](http://www-i6.informatik.rwth-aachen.de/~dreuw/database-rwth-boston-104.php)). In this video, the right-hand 'x' and 'y' locations are plotted as the speaker signs the sentence. The raw data, train, and test sets are pre-defined.

In the first part of the project, a variety of feature sets are derived. Further, in Part-2, three different model selection criterion is implemented. The objective of Model Selection is to tune the number of states for each word HMM before testing on unseen data. In three methods: Log-likelihood using cross-validation folds (CV), Bayesian Information Criterion (BIC), Discriminative Information Criterion (DIC) are explored. Finally, the recognizer is and compare the effects the different combinations of feature sets and model selection criteria.

### Data Description
The data in the `/data/` directory was derived from the RWTH-BOSTON-104 Database. The hand positions (`hand_condensed.csv`) are pulled directly from the database `boston104.handpositions.rybach-forster-dreuw-2009-09-25.full.xml.`

The three markers are:
- `0`: speaker's left hand
- `1`: speaker's right hand
- `2`: speaker's nose
- `X` & `Y` values of the video frame increase left-to-right and top-to-bottom.

For purposes of this project, the sentences have been pre-segmented into words based on slow motion examination of the files. These segments are provided in the `train_words.csv` and `test_words.csv` files in the form of start and end frames (inclusive).

The videos in the corpus include recordings from three different ASL speakers. The mappings for the three speakers to video are included in the `speaker.csv` file.

## Requirements
This project requires **Python 3** with `NumPy`, `Pandas`, `matplotlib`, `SciPy`, `scikit-learn`, `jupyter` and `hmmlearn`.

It is recommended to use [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.

`hmmlearn`, Version 0.2.1, contains a bug-fix related to the log function, which is used in this project. This version can be directly from its repo with the following command:

`pip install git+https://github.com/hmmlearn/hmmlearn.git`

## Files
- `asl_recognizer.ipynb` - Main project notebook.

- `asl_recognizer.html` – HTML export of the main notebook.

- `my_model_selectors.py` – Contains model-selection class.

- `my_recognizer.py` – Implements the recognizer.

## License
[Modified MIT License © Pranav Suri](/License.txt)
