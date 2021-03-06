import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib import rc
from scipy import stats, special
import sys, glob

rc('font',**{'family':'serif'})

m0 = 100.0
beta = 1.0/m0

def Histogram(file):
    data = np.loadtxt(file)
    Nbins = int(np.mean(data))

    plt.figure('p5a')
    plt.hist(data, bins=Nbins, facecolor='b')
    plt.title('Number of agents with a certain capital after transactions', size=14)
    plt.xlabel(r'Money, $m$', size=14)
    plt.ylabel('Number of agents', size=14)
    plt.savefig('Plots/Histogram.png')

def Gibbs(file):
    data = np.loadtxt(file)

    wm = beta*np.exp(-beta*data)

    plt.figure('p5b')
    plt.semilogy(data, wm, '-b')
    plt.xlabel(r'Money, $m$', size=14)
    plt.ylabel(r'$w_m$', size=14)
    plt.title('Gibbs distribution', size=14)
    plt.savefig('Plots/Gibbs_distribution.png')

    plt.figure('p5b_loglog')
    plt.loglog(data, wm, '-b')
    plt.xlabel(r'Money, $m$', size=14)
    plt.ylabel(r'$w_m$', size=14)
    plt.title('Gibbs distribution', size=14)
    plt.savefig('Plots/Gibbs_distribution_loglog.png')


def WithSaving(files):
    lmbd = [0.0, 0.25, 0.5, 0.75, 0.9]
    color = ['b', 'r', 'g', 'k', 'y']
    for ind, file in enumerate(files):
        data = np.loadtxt(file)
        Nbins = int(np.mean(data))
        name = file.split('.')[0]
        name = name.split('L')[-1]

        x = data/m0
        n = 1.0 + 3.0*lmbd[ind]/(1.0-lmbd[ind])
        an = n**n / special.gamma(n)
        P = an * x**(n-1.0) * np.exp(-n*x)

        values, bin = np.histogram(data/m0, bins=Nbins, normed=True)
        print 'Sum under the graph:', sum(np.diff(bin)*values)
        bin_centers = (bin[:-1] + bin[1:])/2.0

        plt.figure('savings')
        plt.plot(data/m0, P, c=color[ind], label=r'$\lambda=%g$'%(lmbd[ind]))
        plt.errorbar(bin_centers[0::5], values[0::5], yerr=0, fmt='.', color=color[ind])
        plt.xlabel(r'$m/m_0$', size=14)
        plt.ylabel('Number of agents, normalized', size=14)
        plt.title('With savings after transactions', size=14)
        plt.legend(loc=1, fontsize=12)
        plt.xlim(0,4)
        plt.savefig('Plots/Savings.png')

        plt.figure('savings log')
        plt.loglog(data/m0, P, c=color[ind], label=r'$\lambda=%g$'%(lmbd[ind]))
        plt.errorbar(bin_centers[0::5], values[0::5], yerr=0, fmt='.', color=color[ind])
        plt.xlabel(r'$m/m_0$', size=14)
        plt.ylabel('Number of agents, normalized', size=14)
        plt.title('With savings after transactions', size=14)
        plt.legend(loc=1, fontsize=12)
        plt.xlim(0.1,4)
        plt.ylim(0.1,3)
        plt.savefig('Plots/Savings_log.png')

def plot5d(files1, files2, label):
    alpha = [0.5, 1.0, 1.5, 2.0]
    color = ['b', 'r', 'g', 'm']
    tail = 0
    f, (ax1, ax2) = plt.subplots(2,1, figsize=(6,6))
    #f2, ax3 = plt.subplots()
    f2, (ax3,ax4) = plt.subplots(2,1, sharex=True, figsize=(6,6))
    f3, ax5 = plt.subplots()
    for ind in range(len(files1)):

        data1 = np.loadtxt(files1[ind])     # No saving
        data2 = np.loadtxt(files2[ind])     # Saving
        N = len(data1)

        w_m1, bins1 = np.histogram(data1/m0, bins=N/10, normed=True)
        w_m2, bins2 = np.histogram(data2/m0, bins=N/10, normed=True)

        ax1.loglog(data1[0::10], w_m1/float(N), c=color[ind], linestyle='--', label=r'$\alpha=%g$'%alpha[ind])
        #ax1.set_xlabel(r'$m/m_0$', size=14)
        ax1.set_ylabel(r'$w_m/N_{agents}$', size=14)
        ax1.legend(loc=1, fontsize=12)
        ax1.set_title('Nearest neighbourgh interaction, N=%d'%N, size=14)

        ax2.loglog(data2[0::10], w_m2/float(N), c=color[ind], linestyle='--', label=r'$\alpha=%g$'%alpha[ind])
        ax2.set_xlabel(r'$m/m_0$', size=14)
        ax2.set_ylabel(r'With saving, $w_m/N_{agents}$', size=14)
        ax2.legend(loc=1, fontsize=12)

        x = data1/m0
        n = 1.0 + 3.0*alpha[ind]/(1.0+alpha[ind])
        an = n**(n) / special.gamma(n)
        P = x**(-n-1.0) * an * np.exp(-n*x)
        tail, bins3 = np.histogram(data1/m0, bins=N/5, normed=True)

        ax3.loglog(data1[0::10], w_m1/float(N), c=color[ind], linestyle='-')
        ax3.loglog(data1, 10*data1**(-1.-alpha[ind])/m0, c=color[ind], linestyle=':', label=r'$m^{-1-\alpha}, \alpha=%g$'%alpha[ind])
        #ax3.set_xlabel(r'$m/m_0$', size=14)
        ax3.set_ylabel(r'$w_m/N_{agents}$', size=14)
        ax3.legend(loc=3, fontsize=12, bbox_to_anchor=(0., 0.98, 1., .102), ncol=2, mode='expand')
        ax3.grid('on')
        ax3.set_xlim(1e1,2e2)
        ax3.set_ylim(8e-6, 1e-3)

        ax4.loglog(data2[0::10], w_m2/float(N), c=color[ind], linestyle='-', label=r'$m^{-1-\alpha}, \alpha=%g$'%alpha[ind])
        ax4.loglog(data2, 10*data2**(-1.-alpha[ind])/m0, c=color[ind], linestyle=':')
        ax4.set_xlabel(r'$m/m_0$', size=14)
        ax4.set_ylabel(r'With saving, $w_m/N_{agents}$', size=14)
        #ax4.legend(loc=3, fontsize=12)
        ax4.grid('on')
        ax4.set_xlim(1e1,2e2)
        ax4.set_ylim(1e-5, 3e-3)


        ax5.loglog(data2[0::10], w_m2/float(N), c=color[ind], linestyle='-')
        ax5.loglog(data2, 30*data2**(-1.-alpha[ind]-0.5)/m0, c=color[ind], linestyle=':', label=r'$\alpha=%g,m^{-1-\alpha-\lambda}$'%alpha[ind])
        ax5.set_xlabel(r'$m/m_0$', size=14)
        ax5.set_ylabel(r'$w_m/N_{agents}$', size=14)
        ax5.set_title(r'Tail fitting with: $\lambda=0.5, \alpha=\{%g, %g, %g, %g\}$'%(alpha[0],alpha[1],alpha[2],alpha[3]))
        ax5.legend(loc=1, fontsize=12)
        ax5.grid('on')
        ax5.set_xlim(1e1,2e2)
        ax5.set_ylim(1e-5, 3e-3)


    f2.subplots_adjust(hspace=0.03)

    f.savefig('Plots/Part_d_%s.png'%label)
    #f2.savefig('Plots/Part_d_powlaw_%s.png'%label)
    f3.savefig('Plots/Part_d_powlaw_with_saving_%s.png'%label)
    f2.savefig('Plots/Powlaw_part_d_%s.png'%label)


def Plot5e(files, a):
    """
    Input: list of data files and the value of alpha
    """

    gamma = [0.0, 1.0, 2.0, 3.0, 4.0]
    color = ['b', 'r', 'g', 'm', 'c']
    lmbd = [0, 0.5]
    j=0

    f, (ax1, ax2) = plt.subplots(1,2, figsize=(7,5))
    f.suptitle(r'Neighbouring interaction, $\alpha = %g$, with and without saving'%(a), fontsize=14)
    for ind,file in enumerate(files):
        name = file.split('_')
        for i in range(len(name)):
            if name[i] == 'L00':

                data = np.loadtxt(file)
                N = len(data)
                Nbins = int(np.mean(data))
                w_m, bins = np.histogram(data/m0, bins=N/10, normed=True)

                ax1.loglog(data[0::10], w_m, c=color[ind], linestyle='--', label=r'$\gamma=%d$'%gamma[ind])
                ax1.set_xlabel(r'$m/m_0$', size=14)
                ax1.set_ylabel(r'$w_m/N_{agents}$', size=14)
                ax1.legend(loc=3, ncol=1, fontsize=12)
                ax1.set_title(r'With no saving, $\lambda = %g$'%(lmbd[0]))
                ax1.set_xlim(3e-3, 100)
                ax1.set_ylim(5e-3,1e1)


            if name[i] == 'L05':

                data = np.loadtxt(file)
                N = len(data)
                Nbins = int(np.mean(data))
                w_m, bins = np.histogram(data/m0, bins=N/10, normed=True)

                ax2.loglog(data[0::10], w_m, c=color[j], linestyle='--', label=r'$\gamma=%d$'%gamma[j])
                ax2.set_xlabel(r'$m/m_0$', size=14)
                #ax2.set_ylabel(r'$w_m/N_{agents}$', size=14)
                ax2.legend(loc=3, ncol=1, fontsize=12)
                ax2.set_title(r'With saving, $\lambda = %g$'%(lmbd[1]))
                ax2.set_xlim(0, 200)

                j += 1


    f.savefig('Plots/Wealth_e_alpha1.png')


###### --- Function calls --- #######

file = glob.glob('Txt_files/*.txt')
saving_files = glob.glob('Txt_files/part_c/*.txt')
NoSaving1000 = glob.glob('Txt_files/part_d/NoSaving/N1000/*.txt')
NoSaving500 = glob.glob('Txt_files/part_d/NoSaving/N500/*.txt')
Saving1000 = glob.glob('Txt_files/part_d/Saving/N1000/*.txt')
Saving500 = glob.glob('Txt_files/part_d/Saving/N500/*.txt')
gamma_files = glob.glob('Txt_files/part_e/*.txt')

#Histogram(file[0])
#Gibbs(file[0])
#WithSaving(saving_files)
plot5d(NoSaving1000, Saving1000, 'N1000')
#plot5d(NoSaving500, Saving500, 'N500')
#Plot5e(gamma_files, 1.0)

plt.show()
