package com.urlshortner.util;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class Base62EncoderTest {

    @Test
    void shouldEncodeAndDecodeRepresentativeValues() {
        assertRoundTrip(0L, "0");
        assertRoundTrip(1L, "1");
        assertRoundTrip(61L, "Z");
        assertRoundTrip(62L, "10");
        assertRoundTrip(3843L, "ZZ");
        assertRoundTrip(3844L, "100");
        assertRoundTrip(999_999_999L, Base62Encoder.encode(999_999_999L));
    }

    @Test
    void shouldRejectInvalidDecodeInput() {
        assertThrows(IllegalArgumentException.class, () -> Base62Encoder.decode(""));
        assertThrows(IllegalArgumentException.class, () -> Base62Encoder.decode("*"));
    }

    @Test
    void shouldRejectNegativeEncodeInput() {
        assertThrows(IllegalArgumentException.class, () -> Base62Encoder.encode(-1));
    }

    private void assertRoundTrip(long numericValue, String expectedEncoded) {
        assertEquals(expectedEncoded, Base62Encoder.encode(numericValue));
        assertEquals(numericValue, Base62Encoder.decode(expectedEncoded));
    }
}

