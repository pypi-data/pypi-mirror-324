# Maximum depositional age calculations
# Heavily influenced by Coutts 2019, dzMDA (Sundell), and detritalPy (Sharman)

from dz_lib.univariate.data import Grain, Sample
from dz_lib.univariate import distributions
import numpy as np
import scipy.stats as stats
import peakutils

# MDA functions:
def youngest_single_grain(grains: [Grain]) -> Grain:
    sorted_grains = sorted(grains, key=lambda grain: grain.age)
    return sorted_grains[0]

def youngest_cluster_1s(
        grains: [Grain],
        min_cluster_size: int = 3,
        contiguous: bool = True
) -> (Grain, float, int):
    sorted_grains = sorted(grains, key=lambda grain: grain.age + grain.uncertainty)
    youngest_cluster = get_youngest_cluster(
        grains=sorted_grains,
        min_cluster_size=min_cluster_size,
        contiguous=contiguous
    )
    if not youngest_cluster:
        return None, float('nan'), 0
    weighted_mean, uncertainty, mswd = get_weighted_mean(
        grains=youngest_cluster,
        confidence_level=0.95
    )
    weighted_grain = Grain(age=weighted_mean, uncertainty=uncertainty)
    return weighted_grain, mswd, len(youngest_cluster)

def youngest_cluster_2s(
        grains: [Grain],
        min_cluster_size: int = 3,
        contiguous: bool = True
    ) -> (Grain, float, int):
    for grain in grains:
        grain.uncertainty += grain.uncertainty
    sorted_grains = sorted(grains, key=lambda grain: grain.age + grain.uncertainty)
    youngest_cluster = get_youngest_cluster(
        grains=sorted_grains,
        min_cluster_size=min_cluster_size,
        contiguous=contiguous
    )
    if not youngest_cluster:
        return None, float('nan'), 0
    for grain in youngest_cluster:
        grain.uncertainty -= grain.uncertainty
    weighted_mean, uncertainty, mswd = get_weighted_mean(
        grains=youngest_cluster,
        confidence_level=0.95
    )
    weighted_grain = Grain(age=weighted_mean, uncertainty=uncertainty)
    return weighted_grain, mswd, len(youngest_cluster)

def youngest_3_zircons(grains: [Grain]) -> (Grain, float):
    if len(grains) < 3:
        return None, float('nan')
    sorted_grains = sorted(grains, key=lambda grain: grain.age)
    youngest_three = sorted_grains[:3]
    weighted_mean, uncertainty, mswd = get_weighted_mean(
        grains=youngest_three,
        confidence_level=0.95
    )
    weighted_grain = Grain(age=weighted_mean, uncertainty=uncertainty)
    return weighted_grain, mswd

def youngest_3_zircons_overlap(
        grains: [Grain],
        sigma: int = 1,
        contiguous: bool = True
) -> (Grain, float, int):
    if len(grains) < 3:
        return None, float('nan'), 0
    sorted_grains = sorted(grains, key=lambda grain: grain.age + sigma * grain.uncertainty)
    youngest_cluster = get_youngest_cluster(
        grains=sorted_grains,
        min_cluster_size=3,
        add_uncertainty=True,
        contiguous=contiguous
    )
    if not youngest_cluster or len(youngest_cluster) < 3:
        return None, float('nan'), 0
    weighted_mean, uncertainty, mswd = get_weighted_mean(
        grains=youngest_cluster,
        confidence_level=0.95
    )
    weighted_grain = Grain(age=weighted_mean, uncertainty=uncertainty)
    return weighted_grain, mswd, len(youngest_cluster)

def youngest_graphical_peak(
        grains: [Grain],
        min_cluster_size: int = 2,
        threshold: float = 0.01,
        min_dist: float = 1.0
) -> float:
    distro = distributions.pdp_function(Sample("temp", grains))
    points = sorted(zip(distro.x_values, distro.y_values), key=lambda p: p[0])
    ages, probabilities = zip(*points)
    peak_indexes = list(peakutils.indexes(np.array(probabilities), thres=threshold, min_dist=int(min_dist)))
    if not peak_indexes:
        return float('nan')
    peak_ages = [ages[i] for i in peak_indexes]
    valid_peaks = [
        (age, count_bins_around_peak(age, distro))
        for age in peak_ages
    ]
    valid_peaks = [(age, count) for age, count in valid_peaks if count >= min_cluster_size]
    if not valid_peaks:
        return float('nan')
    return round(min(valid_peaks, key=lambda p: p[0])[0], 1)

def youngest_statistical_population(
    grains: [Grain],
    min_cluster_size: int = 2,
    mswd_threshold: float = 1.0,
    sigma: float = 1.0,
    add_uncertainty: bool=False
) -> (Grain, float, int):
    if add_uncertainty:
        sorted_grains = sorted(grains, key=lambda g: g.age + sigma * g.uncertainty)
    else:
        sorted_grains = sorted(grains, key=lambda g: g.age)
    best_grain = None
    best_mswd = float('nan')
    best_count = 0
    for j in range(len(sorted_grains) - min_cluster_size + 1):
        subset = sorted_grains[: j + min_cluster_size]
        wm_age, wm_err2s, mswd = get_weighted_mean(subset)
        if j == 0 and mswd > mswd_threshold:
            continue
        if abs(mswd - 1) < abs(best_mswd - 1) if not np.isnan(best_mswd) else True:
            best_grain = Grain(age=wm_age, uncertainty=wm_err2s)
            best_mswd = mswd
            best_count = len(subset)
        if mswd > 1:
            break
    return best_grain, best_mswd, best_count if best_grain else (None, float('nan'), 0)

def tau_method(
    grains: [Grain],
    min_cluster_size: int = 3,
    thres: float = 0.01,
    min_dist: int = 1,
) -> (Grain, float, int):
    distro = distributions.pdp_function(Sample("temp", grains))
    x_values = distro.x_values
    y_values = distro.y_values
    trough_indexes = list(peakutils.indexes(-y_values, thres=thres, min_dist=min_dist))
    trough_ages = [0] + list(x_values[trough_indexes]) + [max(x_values)]
    grains_in_troughs = [
        [g for g in grains if trough_ages[j] <= g.age <= trough_ages[j + 1]]
        for j in range(len(trough_ages) - 1)
    ]
    valid_clusters = [i for i, cluster in enumerate(grains_in_troughs) if len(cluster) >= min_cluster_size]
    if not valid_clusters:
        return None, float('nan'), 0
    youngest_index = valid_clusters[0]
    selected_grains = grains_in_troughs[youngest_index]
    tau_WM, tau_WM_err2s, tau_WM_MSWD = get_weighted_mean(selected_grains)
    return Grain(age=tau_WM, uncertainty=tau_WM_err2s), tau_WM_MSWD, len(selected_grains)


# MDA utils:
def count_bins_around_peak(peak_age: float, distribution: distributions.Distribution, window: float = 1.0) -> int:
    return sum(1 for x in distribution.x_values if abs(x - peak_age) <= window / 2)

def get_youngest_cluster(
        grains: [Grain],
        min_cluster_size: int,
        add_uncertainty: bool = False,
        contiguous: bool = True
) -> [Grain]:
    if add_uncertainty:
        sorted_grains = sorted(grains, key=lambda grain: grain.age + grain.uncertainty)
    else:
        sorted_grains = sorted(grains, key=lambda grain: grain.age)

    ages_plus_uncertainties = [grain.age + grain.uncertainty for grain in sorted_grains]
    ages_minus_uncertainties = [grain.age - grain.uncertainty for grain in sorted_grains]

    for i, grain in enumerate(sorted_grains):
        overlaps = [
            ages_minus_uncertainties[j] < ages_plus_uncertainties[i]
            for j in range(i, len(sorted_grains))
        ]
        if not contiguous:
            if sum(overlaps) >= min_cluster_size:
                return [sorted_grains[j] for j, overlap in enumerate(overlaps, start=i) if overlap]
        else:
            false_indices = [k for k, overlap in enumerate(overlaps) if not overlap]
            if not false_indices:
                if len(sorted_grains[i:]) >= min_cluster_size:
                    return sorted_grains[i:]
            elif false_indices[0] >= min_cluster_size:
                return sorted_grains[i:i + false_indices[0]]
    return []

def get_weighted_mean(
        grains: [Grain],
        confidence_level: float=0.95
) -> (float, float, float):
    ages = np.array([grain.age for grain in grains])
    uncertainties = np.array([grain.uncertainty for grain in grains])
    weights = uncertainties**(-2)
    normalized_weights = weights / np.sum(weights)
    weighted_mean = np.sum(normalized_weights * ages)
    s = np.sum(((ages - weighted_mean)**2) / uncertainties**2)
    n = len(ages)
    mswd = s / (n - 1)
    z_score = stats.norm.ppf(confidence_level + (1 - confidence_level) / 2.0)
    two_sigma_uncertainty = z_score * np.sqrt(1 / np.sum(weights))
    return weighted_mean, two_sigma_uncertainty, mswd