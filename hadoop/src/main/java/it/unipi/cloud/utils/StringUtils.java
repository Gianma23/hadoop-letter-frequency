package it.unipi.cloud.utils;

import java.text.Normalizer;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class StringUtils {

    static Pattern pattern = Pattern.compile("^[A-Za-z]+$");

    private StringUtils() {
        throw new IllegalStateException("Static utility class cannot be instantiated");
    }

    static public String normalizeString(String text) {
        text = Normalizer.normalize(text, Normalizer.Form.NFD);
        return text.replaceAll("\\p{M}", "");
    }

    static public boolean isLetter(String text) {
        Matcher matcher = pattern.matcher(text);
        return matcher.matches();
    }
}
