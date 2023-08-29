 odoo.define('pos_restaurant_depends_bits.FloorScreenMenu', function (require) {
  'use strict';

  const PosComponent = require('point_of_sale.PosComponent');
  const Registries = require('point_of_sale.Registries'); 

  class FloorScreenMenu extends PosComponent {
    async onClick() {  
      this.showScreen('FloorScreen');
    } 
  }
  FloorScreenMenu.template = 'FloorScreenMenu';
  Registries.Component.add(FloorScreenMenu); 
  return FloorScreenMenu
});
