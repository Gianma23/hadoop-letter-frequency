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

import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class MapReduceApp {

    private static final int INPUT_INDEX = 0;
    private static final int OUTPUT_LETTERCOUNT_INDEX = 1;
    private static final int OUTPUT_LETTERFREQ_INDEX = 2;
    private static final int NUMBER_OF_REDUCERS_INDEX = 3;
    private static final int METHOD_INDEX = 4;

    @SuppressWarnings("unchecked")
    public static void main(String[] args) throws Exception{
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();

        if(otherArgs.length != 5){
            System.err.println("Usage: letterfrequency <input> <letterTotalCountOutput> <letterFrequencyOutput> <nReducers> <method>");
            System.exit(2);
        }
        String inputhPath = otherArgs[INPUT_INDEX];
        String outputLetterCountPath = otherArgs[OUTPUT_LETTERCOUNT_INDEX]; 
        String outputLetterFreqPath = otherArgs[OUTPUT_LETTERFREQ_INDEX];
        int nReducers = Integer.parseInt(otherArgs[NUMBER_OF_REDUCERS_INDEX]);
        String method = "it.unipi.cloud." + otherArgs[METHOD_INDEX];

        // Start the job to count the total number of letters
        Job countJob = Job.getInstance(conf, "Total Letter Count");
        countJob.setJarByClass(Class.forName(method + ".LetterTotalCount"));
        countJob.setMapperClass((Class<Mapper>) Class.forName(method + ".LetterTotalCount$CounterMapper"));
        countJob.setCombinerClass((Class<Reducer>) Class.forName(method + ".LetterTotalCount$CounterReducer"));
        countJob.setReducerClass((Class<Reducer>) Class.forName(method + ".LetterTotalCount$CounterReducer"));
        
        countJob.setOutputKeyClass(Text.class);
        countJob.setOutputValueClass(LongWritable.class);

        FileInputFormat.addInputPath(countJob, new Path(inputhPath));
        FileOutputFormat.setOutputPath(countJob, new Path(outputLetterCountPath));

        if(!countJob.waitForCompletion(true)){
            System.exit(1);
        }

        // Start the job to calculate the frequency of each letter
        Job freqJob = Job.getInstance(conf, "Letter Frequency");
        
        long letterCount = getLetterCount(conf, outputLetterCountPath);
        freqJob.getConfiguration().setLong("letterCount", letterCount);
        
        freqJob.setJarByClass(Class.forName(method + ".LetterFrequency"));
        freqJob.setMapperClass((Class<Mapper>) Class.forName(method + ".LetterFrequency$CounterMapper"));
        freqJob.setCombinerClass((Class<Reducer>) Class.forName(method + ".LetterFrequency$CounterReducer"));
        freqJob.setReducerClass((Class<Reducer>) Class.forName(method + ".LetterFrequency$CounterReducer"));

        freqJob.setNumReduceTasks(nReducers);

        freqJob.setMapOutputKeyClass(Text.class);
        freqJob.setMapOutputValueClass(LongWritable.class);
        freqJob.setOutputKeyClass(Text.class);
        freqJob.setOutputValueClass(DoubleWritable.class);

        FileInputFormat.addInputPath(freqJob, new Path(inputhPath));
        FileOutputFormat.setOutputPath(freqJob, new Path(outputLetterFreqPath));

        System.exit(freqJob.waitForCompletion(true) ? 0 : 1);
    }

    private static long getLetterCount(Configuration conf, String outputDir) throws IOException {
        FileSystem fs = FileSystem.get(conf);
        Path outputPath = new Path(outputDir);
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
            
            String firstLine = bufferedReader.readLine();
            if (firstLine != null) {
                firstLine = firstLine.split("\t")[1];
                letterCount += Long.parseLong(firstLine);                    
            }
            // Close the input stream
            bufferedReader.close();
            inputStream.close();
        }
        return letterCount;
    }
}