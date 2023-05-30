#include "bn_core.h"

#include "map.hpp"



int main() {
    bn::core::init();

    bn::animation::map anim = bn::animation::map(10);
    
    while (true) {
        anim2.update();
        // anim.update();
        //bg_map_ptr.update();
        bn::core::update();
    }
}

