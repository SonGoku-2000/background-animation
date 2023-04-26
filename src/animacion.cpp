#include "animacion.hpp"


#include "bn_memory.h"
namespace anim {

    Animacion::Animacion(int wait_updates):
        map_item(cells[0], bn::size(columns, rows)),
        bg_item(bn::regular_bg_tiles_items::tiles,
            bn::bg_palette_items::palette,
            map_item),
        bg(bg_item.create_bg(0, 0)) ,
        bg_map(bg.map()){

        wait = wait_updates;
        bg_map.reload_cells_ref();
    }

    void Animacion::update() {
        if (cells[0] == 0) {
            bn::memory::copy(patron1[0], cells_count, cells[0]);
        }
        else {
            bn::memory::copy(patron2[0], cells_count, cells[0]);
        }

        bg_map.reload_cells_ref();
    }

    void Animacion::reset() {
        bn::memory::copy(patron1[0], cells_count, cells[0]);
    }
}