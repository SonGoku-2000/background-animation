#include "animacion.hpp"


#include "bn_memory.h"
namespace anim{

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
}