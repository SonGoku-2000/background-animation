#include "animacion.hpp"


#include "bn_memory.h"

#include "bn_log.h"
namespace bn {
    namespace animation {

        Animation::Animation(int wait_updates) :
            map_item(cells[0], bn::size(columns, rows)),
            bg_item(bn::regular_bg_tiles_items::tiles2,
                bn::bg_palette_items::tiles2_palette,
                map_item),
            bg(bg_item.create_bg(0, 0)),
            bg_map(bg.map()) {

            wait = wait_updates;
            bg_map.reload_cells_ref();
        }

        void Animation::update() {
            if (cont < wait) {
                cont++;
                return;
            }
            cont = 1;

            if (frameActual == 1) {
                bn::memory::copy(patron1[0], cells_count, cells[0]);
            }
            else if (frameActual == 2) {
                bn::memory::copy(patron2[0], cells_count, cells[0]);
            }
            else {
                BN_LOG("error frame no contabilizado");
            }

            frameActual++;

            if (frameActual > framesTotales) {
                frameActual = 1;
            }

            bg_map.reload_cells_ref();
        }

        void Animation::reset() {
            bn::memory::copy(patron1[0], cells_count, cells[0]);
        }
    }
}