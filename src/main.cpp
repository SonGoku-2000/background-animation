/*
 * Copyright (c) 2020-2023 Gustavo Valiente gustavo.valiente@protonmail.com
 * zlib License, see LICENSE file.
 */

#include "bn_core.h"

#include "animacion.hpp"



int main() {
    bn::core::init();

    anim::Animacion bg_map_ptr = anim::Animacion(10);
    
    while (true) {
        bg_map_ptr.update();
        bn::core::update();
    }
}

