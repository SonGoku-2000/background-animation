/*
 * Copyright (c) 2020-2023 Gustavo Valiente gustavo.valiente@protonmail.com
 * zlib License, see LICENSE file.
 */

#include "bn_core.h"
#include "bn_keypad.h"
#include "bn_memory.h"
#include "bn_regular_bg_ptr.h"
#include "bn_regular_bg_item.h"
#include "bn_regular_bg_map_ptr.h"
#include "bn_regular_bg_map_cell_info.h"

#include "bn_bg_palette_items_palette.h"
#include "bn_regular_bg_tiles_items_tiles.h"

#include "animacion.hpp"



int main() {
    bn::core::init();

    bg_map bg_map_ptr = bg_map();
    bn::regular_bg_item bg_item(
        bn::regular_bg_tiles_items::tiles, bn::bg_palette_items::palette, bg_map_ptr.map_item);
    bn::regular_bg_ptr bg = bg_item.create_bg(0, 0);
    bn::regular_bg_map_ptr bg_map = bg.map();

    bg_map.reload_cells_ref();
    while (true) {
        bg_map_ptr.update();
        bg_map.reload_cells_ref();
        bn::core::update();
    }
}

