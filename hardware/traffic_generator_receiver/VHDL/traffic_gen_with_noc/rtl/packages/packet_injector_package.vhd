-------------------------------------------------------------------------------
-- Title      : 
-- Project    : 
-------------------------------------------------------------------------------
-- File       : packet_injector_package.vhd
-- Author     : Behnam Razi Perjikolaei  <raziperj@uni-bremen.de>
-- Company    : 
-- Created    : 2019-06-20
-- Last update: 2019-06-24
-- Platform   : 
-- Standard   : VHDL'87
-------------------------------------------------------------------------------
-- Description: 
-------------------------------------------------------------------------------
-- Copyright (c) 2019 
-------------------------------------------------------------------------------
-- Revisions  :
-- Date        Version  Author  Description
-- 2019-06-20  1.0      behnam  Created
-------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.math_real.all;
use ieee.numeric_std.all;
use work.NOC_3D_PACKAGE.all;
------------------------------------------------------------------------------------------

package packet_injector_package is
  constant max_packet_num           : positive := 31;
  function rand_destination (seed_1 : positive; seed_2 : positive; layer_prob : integer_vec)
    return address_inf;
  function find_int (int_vec : integer_vec; int_val : integer)
    return boolean;
  

end packet_injector_package;

------------------------------------------------------------------------------------------

package body packet_injector_package is

  -- purpose: generate random node address by considering probability of each layer
  function rand_destination (
    seed_1     : positive;
    seed_2     : positive;
    layer_prob : integer_vec)
    return address_inf is
    variable x_rand, y_rand, z_rand             : real;
    variable x_range                            : real := real(max_x_dim);
    variable y_range                            : real := real(max_y_dim);
    variable z_range                            : real := 100.0;
    variable z_prob_min, z_prob_max             : integer range 0 to 100;
    variable x_rand_num, y_rand_num, z_rand_num : integer range 0 to 100;
    variable dest_addr                          : address_inf;
    variable seed1, seed2                       : positive;
  begin  -- rand_destination
    seed1      := seed_1;
    seed2      := seed_2;
    uniform(seed1, seed2, z_rand);
    z_rand_num := integer(z_rand*z_range);
    uniform(seed1, seed2, y_rand);
    y_rand_num := integer(y_rand*y_range);
    uniform(seed1, seed2, x_rand);
    x_rand_num := integer(x_rand*x_range);
    z_prob_max := 0;
    for i in layer_prob'range loop
      z_prob_min    := z_prob_max;
      z_prob_max    := z_prob_min+layer_prob(i);
      if z_rand_num <= z_prob_max and z_rand_num >= z_prob_min then
        dest_addr.z_dest := std_logic_vector(to_unsigned(i, positive(ceil(log2(real(max_z_dim))))));
        dest_addr.y_dest := std_logic_vector(to_unsigned(y_rand_num, positive(ceil(log2(real(max_y_dim))))));
        dest_addr.x_dest := std_logic_vector(to_unsigned(x_rand_num, positive(ceil(log2(real(max_x_dim))))));
      end if;
    end loop;  -- i
    return dest_addr;
  end rand_destination;

  -- purpose: find an integer value in an integer vector and return true or false
  function find_int (
    int_vec : integer_vec;
    int_val : integer)
    return boolean is
    variable find_result : boolean := false;
  begin  -- find_int
    for i in 0 to int_vec'length-1 loop
      if int_vec(i) = int_val then
        find_result := true;
      end if;
    end loop;  -- i
    return find_result;
  end find_int;
end packet_injector_package;
------------------------------------------------------------------------------------------
