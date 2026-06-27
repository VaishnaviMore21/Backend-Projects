package com.urlshortner.util;

import java.util.HashMap;
import java.util.Map;

public final class Base62Encoder {

    private static final String ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    private static final int BASE = ALPHABET.length();
    private static final Map<Character, Integer> CHAR_TO_VALUE = new HashMap<Character, Integer>();

    static {
        for (int i = 0; i < ALPHABET.length(); i++) {
            CHAR_TO_VALUE.put(ALPHABET.charAt(i), i);
        }
    }

    private Base62Encoder() {
    }

    /**
     * Converts a numeric database identifier into a compact Base62 string.
     *
     * Example: 62 -> "10"
     * We repeatedly divide the number by 62 and prepend the matching character
     * from the Base62 alphabet, which produces a short, URL-safe code.
     */
    public static String encode(long value) {
        if (value < 0) {
            throw new IllegalArgumentException("Base62 encoding only supports non-negative values");
        }

        if (value == 0) {
            return String.valueOf(ALPHABET.charAt(0));
        }

        StringBuilder builder = new StringBuilder();
        long current = value;

        while (current > 0) {
            int remainder = (int) (current % BASE);
            builder.append(ALPHABET.charAt(remainder));
            current = current / BASE;
        }

        return builder.reverse().toString();
    }

    /**
     * Reconstructs the numeric identifier from a Base62 short code.
     * Each character contributes its positional value in base 62, allowing the
     * short code to be deterministically mapped back to the original number.
     */
    public static long decode(String shortCode) {
        if (shortCode == null || shortCode.trim().isEmpty()) {
            throw new IllegalArgumentException("Short code cannot be null or blank");
        }

        long result = 0L;
        for (char character : shortCode.toCharArray()) {
            Integer digit = CHAR_TO_VALUE.get(character);
            if (digit == null) {
                throw new IllegalArgumentException("Invalid Base62 character: " + character);
            }
            result = (result * BASE) + digit;
        }
        return result;
    }
}

