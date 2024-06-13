package it.unipi.cloud;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.util.GenericOptionsParser;

// TODO conditionally import the correct classes
import it.unipi.cloud.combiner.LetterTotalCount;
import it.unipi.cloud.combiner.LetterFrequency;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class MapReduceApp {

    private static final int NUMBER_OF_REDUCERS = 3;
    private static final int INPUT_INDEX = 0;
    private static final int OUTPUT_LETTERCOUNT_INDEX = 1;
    private static final int OUTPUT_LETTERFREQ_INDEX = 2;

    public static void main(String[] args) throws Exception{
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();

        if(otherArgs.length != 3){
            System.err.println("Usage: letterfrequency <input> <LetterTotalCountOutput> <LetterFrequencyOutput>");
            System.exit(2);
        }

        // Start the job to count the total number of letters
        Job countJob = Job.getInstance(conf, "Total Letter Count");
        countJob.setJarByClass(LetterTotalCount.class);
        countJob.setMapperClass(LetterTotalCount.CounterMapper.class);
        countJob.setCombinerClass(LetterTotalCount.CounterReducer.class);
        countJob.setReducerClass(LetterTotalCount.CounterReducer.class);
        
        countJob.setOutputKeyClass(org.apache.hadoop.io.Text.class);
        countJob.setOutputValueClass(org.apache.hadoop.io.LongWritable.class);

        FileInputFormat.addInputPath(countJob, new Path(otherArgs[INPUT_INDEX]));
        FileOutputFormat.setOutputPath(countJob, new Path(otherArgs[OUTPUT_LETTERCOUNT_INDEX]));

        if(!countJob.waitForCompletion(true)){
            System.exit(1);
        }

        // Start the job to calculate the frequency of each letter
        Job freqJob = Job.getInstance(conf, "Letter Frequency");
        
        long letterCount = getLetterCount(conf, otherArgs[OUTPUT_LETTERCOUNT_INDEX]);
        freqJob.getConfiguration().setLong("letterCount", letterCount);
        
        freqJob.setJarByClass(LetterFrequency.class);
        freqJob.setMapperClass(LetterFrequency.CounterMapper.class);
        freqJob.setCombinerClass(LetterFrequency.CounterReducer.class);
        freqJob.setReducerClass(LetterFrequency.CounterReducer.class);

        freqJob.setNumReduceTasks(NUMBER_OF_REDUCERS);

        countJob.setOutputKeyClass(org.apache.hadoop.io.Text.class);
        countJob.setOutputValueClass(org.apache.hadoop.io.LongWritable.class);

        FileInputFormat.addInputPath(freqJob, new Path(otherArgs[INPUT_INDEX]));
        FileOutputFormat.setOutputPath(freqJob, new Path(otherArgs[OUTPUT_LETTERFREQ_INDEX]));

        System.exit(freqJob.waitForCompletion(true) ? 0 : 1);
    }

    private static long getLetterCount(Configuration conf, String outputDir) throws IOException {
        // Read the output of the first job
        FileSystem fs = FileSystem.get(conf);
        Path outputPath = new Path(outputDir);

        // Initialize the total text length
        long letterCount = 0;

        // Get a list of all files in the output directory
        FileStatus[] status = fs.listStatus(outputPath);
        for (FileStatus fileStatus : status) {
            String fileName = fileStatus.getPath().getName();

            // Ignore the _SUCCESS file
            if (fileName.equals("_SUCCESS")) {
                continue;
            }
            // Open the file
            FSDataInputStream inputStream = fs.open(fileStatus.getPath());
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));

            // The result is on the first line of the output
            String firstLine = bufferedReader.readLine();
            if (firstLine != null) {
                long textLength = Long.parseLong(firstLine);
                letterCount += textLength;                    
            }
            
            // Close the input stream
            bufferedReader.close();
            inputStream.close();
        
        }
        return letterCount;
    }
}