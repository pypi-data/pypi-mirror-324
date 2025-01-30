from setuptools import setup, find_packages

setup(
    name='evalnlp',  # Nom de ta librairie
    version='0.1.2',  # Version mise à jour
    description='Enhanced evaluation metrics for NLP tasks',
    long_description=open('README.md').read(),  # Description longue depuis le README
    long_description_content_type='text/markdown',  # Format du README
    packages=find_packages(),  # Recherche automatiquement tous les sous-modules
    install_requires=[
        'textdistance',
        'jiwer'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.5', 
)
