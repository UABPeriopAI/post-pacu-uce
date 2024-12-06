import pathlib
import click

@click.command()
@click.option('--training_data', 
            type=str,
            help='Pickle file of the pandas dataframe containing ' \
            'paper meta data and z-scores with corresponding' \
            'highly-cited label'\
            )
@click.option('--output_location', 
            type=str,
            help='Folder path for output files, including the saved model'\
            )


def check_stuff(training_data, output_location):
    print("training data = ", training_data)
    print("output destination = ", output_location) 
   
    check_if_empty = pathlib.Path(output_location).iterdir()
    if any(check_if_empty):
        print("Cannot write to non-empty directory")

    

if __name__ == "__main__":
    check_stuff()