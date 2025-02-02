//! algorithms/pesa_ii.rs
//! Implements the Pareto Envelope-based Selection Algorithm II (PESA-II)
//! This Source Code Form is subject to the terms of The GNU General Public License v3.0
//! Copyright 2024 - Guilherme Santos. If a copy of the MPL was not distributed with this
//! file, You can obtain one at https://www.gnu.org/licenses/gpl-3.0.html

mod evolutionary;
mod hypergrid;
mod model_selection;
mod algorithms;
mod reduction;

use crate::graph::{Graph, Partition};
use crate::utils::args::AGArgs;
use hypergrid::{HyperBox, Solution};

/// Main run function that creates both the real and random fronts, then
/// selects the best solution via the chosen criterion.
pub fn run(graph: &Graph, args: AGArgs) -> (Partition, Vec<f64>, f64) {
    match args.multi_level {
        true => {
            return algorithms::multi_level_evolutionary(graph, args);
        }

        false => {
            return  algorithms::single_level(graph, args);
        }

    }
}