#include "animacion.hpp"


#include "bn_memory.h"
namespace anim {

    bg_map::bg_map():
        map_item(cells[0], bn::size(bg_map::columns, bg_map::rows)) {
        reset();
    }

    void bg_map::update() {
        if (cells[0] == 0) {
            bn::memory::copy(patron1[0], cells_count, cells[0]);
        }
        else {
            bn::memory::copy(patron2[0], cells_count, cells[0]);
        }
    }

    void bg_map::reset() {
        bn::memory::copy(patron1[0], cells_count, cells[0]);
    }

    Animacion::Animacion(int wait_updates):
        map_item(cells[0], bn::size(bg_map::columns, bg_map::rows)),
        bg_item(bn::regular_bg_tiles_items::tiles,
            bn::bg_palette_items::palette,
            map_item),
        bg(bg_item.create_bg(0, 0)) {

        wait = wait_updates;

    }

    void Animacion::update() {
        if (cells[0] == 0) {
            bn::memory::copy(patron1[0], cells_count, cells[0]);
        }
        else {
            bn::memory::copy(patron2[0], cells_count, cells[0]);
        }
    }

    void Animacion::reset() {
        bn::memory::copy(patron1[0], cells_count, cells[0]);
    }
}