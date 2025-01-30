#include <nanobind/nanobind.h>

#include <string.h>

#include "sixel.h"

namespace nb = nanobind;
using namespace nb::literals;

struct Outbuf {
    size_t size;
    uint8_t* buf;
};

// Growing output buffer
static int memory_write_callback(char *data, int size, void *priv) {
    Outbuf* buf = (Outbuf*)priv;
    buf->buf = (uint8_t*)realloc(buf->buf, buf->size + size);
    memcpy(buf->buf + buf->size, data, size);
    buf->size += size;
    return size;
}

static nb::bytes sixel_encode_bytes(nb::bytes src_pixels, int width, int height) {
    sixel_encoder_t *encoder;

    uint8_t* pixdata = (uint8_t*)src_pixels.c_str();
    sixel_dither_t* dither;
    sixel_dither_new(&dither, -1, NULL); // no dither
    sixel_dither_initialize(dither,
                            pixdata,
                            width,
                            height,
                            SIXEL_PIXELFORMAT_RGB888,
                            SIXEL_LARGE_NORM,
                            SIXEL_REP_CENTER_BOX,
                            SIXEL_QUALITY_HIGH);

    Outbuf outbuf;
    memset(&outbuf, 0, sizeof(outbuf));

    sixel_output_t *output = NULL;
    sixel_output_new(&output, memory_write_callback, (void *)&outbuf, NULL /* allocator */);

    SIXELSTATUS status = sixel_encode(pixdata, width, height, 3, dither, output);

    auto res = nb::bytes(outbuf.buf, outbuf.size);

    sixel_output_unref(output);
    sixel_dither_unref(dither);

    free(outbuf.buf);
    return res;
}

NB_MODULE(consgfx_ext, m) {
    m.def("sixel_encode_bytes", &sixel_encode_bytes, "pixel_data"_a, "width"_a, "height"_a,
        "Encode 'pixel_data' RGB data (3 bytes per pixel) into sixels format.");
}
